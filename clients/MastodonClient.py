from mastodon import Mastodon
from os.path import isfile
from pathlib import Path
import os
import re
from .ClientStatus import ClientStatus


class MastodonClient(Mastodon):
    def __init__(self, app_name, masto_client_id='', savedata_folder=Path('.'), **kwargs):
        self.status = ClientStatus.DISCONNECTED
        self.masto_client_id = ''

        access_token_file = kwargs.get('access_token_file', False)
        client_cred_file = kwargs.get('client_cred_file', False)
        app_prefix = app_name + '_'
        if client_cred_file and access_token_file:  # Already have login data files: fastforward to access token login
            self.masto_client_id = access_token_file.stem.removeprefix(app_prefix)
            self._InitWithAccessToken(client_cred_file, access_token_file)
            return

        # Supposed to be of the form '@Toot@mastodon.social'
        server_url = masto_client_id.split('@')[2]
        client_cred_file = savedata_folder / (app_prefix + server_url + ".secret")
        client_cred_file.parent.mkdir(exist_ok=True, parents=True)
        if not isfile(client_cred_file):
            # Register the app! This only needs to be done once per device and server.
            Mastodon.create_app(
                app_name,
                api_base_url='https://' + server_url,
                to_file=client_cred_file
            )
        self.access_token_file = savedata_folder / (app_prefix + masto_client_id + ".secret")
        if not isfile(self.access_token_file):
            super(MastodonClient, self).__init__(client_id=client_cred_file)  # Call super here as we needed to initialize client_cred_file and create_app first
            self.status = ClientStatus.NEED_OAUTH_CONNECTION
        else:
            self._InitWithAccessToken(client_cred_file, self.access_token_file)

    """Supposed to be called only from __init__"""
    def _InitWithAccessToken(self, client_cred_file, access_token_file):
        super(MastodonClient, self).__init__(client_id=client_cred_file, access_token=access_token_file)
        self.status = ClientStatus.CONNECTED

    def GetOAuthURL(self):
        return self.auth_request_url()

    def ConnectOAuth(self, code_from_oauth):
        if self.status is not ClientStatus.NEED_OAUTH_CONNECTION:
            return
        self.log_in(
            to_file=self.access_token_file,
            code=code_from_oauth,
            scopes=['read', 'write']
        )
        self.status = ClientStatus.CONNECTED

    def Post(self, message):
        if self.status is not ClientStatus.CONNECTED:
            return
        self.toot(message)

    def IsConnected(self):
        return self.status is ClientStatus.CONNECTED

    @staticmethod
    def LookupExistingClients(app_name, savedata_folder):
        prefix = app_name + "_"
        masto_folder = savedata_folder / "mastodon"
        try:
            matching_files = [f for f in os.listdir(masto_folder) if f.startswith(prefix) and re.search(r'.+_@.+@.+\.secret$', f)]
        except FileNotFoundError:
            matching_files = []  # No data
        if not matching_files:
            return []

        connected_clients = []
        for client_file in matching_files:
            filepath = masto_folder / client_file
            server_url = filepath.stem.split('@')[2]
            client_cred_filepath = masto_folder / (app_name + '_' + server_url + ".secret")
            new_client = MastodonClient(app_name, client_cred_file=client_cred_filepath, access_token_file=filepath)
            connected_clients.append(new_client)
        return connected_clients

    def GetClientName(self):
        return self.masto_client_id
