from blueskysocial import Client, Post
from base64 import b64encode, b64decode
from pathlib import Path
import os
from .ClientStatus import ClientStatus
import re


class BlueskyClient(Client):
    def __init__(self, app_name, savedata_folder, **kwargs):
        super(BlueskyClient, self).__init__()
        self.status = ClientStatus.DISCONNECTED
        self.app_name = app_name
        self.save_folder = savedata_folder
        self.client_name = ''
        user_name = kwargs.get('user_name', None)
        password = kwargs.get('password', None)
        if user_name is not None and password is not None:
            self.Login(user_name, password)
        elif user_name is not None:  # try to read login info from cached file
            self.client_name = user_name
            user_file = savedata_folder / "bluesky" / Path(app_name + "_" + user_name + ".secret")
            try:
                with open(user_file, "r") as file:
                    user = b64decode(file.readline().strip())
                    pwd = b64decode(file.readline().strip())
                    self.Login(user, pwd)
            except FileNotFoundError:
                self.status = ClientStatus.NEED_PASSWORD

    def Login(self, user_name, password):
        self.authenticate(user_name, password)
        self.status = ClientStatus.CONNECTED
        self.client_name = user_name
        # Cache the info for later
        user_file = self.save_folder / "bluesky" / Path(self.app_name + "_" + user_name + ".secret")
        user_file.parent.mkdir(exist_ok=True, parents=True)
        with open(user_file, "w") as file:
            enc_user = b64encode(user_name.encode('ascii')).decode('ascii')
            enc_pwd = b64encode(password.encode('ascii')).decode('ascii')
            file.write("{}\n{}\n".format(enc_user, enc_pwd))

    @staticmethod
    def LookupExistingClients(app_name, savedata_folder):
        prefix = app_name + "_"
        bs_folder = savedata_folder / "bluesky"
        try:
            matching_files = [f for f in os.listdir(bs_folder) if f.startswith(prefix) and re.search(r'.+_.+\.secret$', f)]
        except FileNotFoundError:
            matching_files = []  # No data
        if not matching_files:
            return []

        connected_clients = []
        for client_file in matching_files:
            filepath = bs_folder / client_file
            with open(filepath, "r") as file:
                user = b64decode(file.readline().strip()).decode('ascii')
                pwd = b64decode(file.readline().strip()).decode('ascii')
            new_client = BlueskyClient(app_name, savedata_folder, user_name=user, password=pwd)
            connected_clients.append(new_client)
        return connected_clients

    def Post(self, message):
        post = Post(message)
        self.post(post)

    def GetClientName(self):
        return self.client_name
