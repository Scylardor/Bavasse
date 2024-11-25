from clients import ClientStatus


class NewClientController(object):
    def __init__(self, view, new_client_callback, connected_clients):
        self.opened_menu = False
        self.new_client_cb = new_client_callback
        self.connected_clients = connected_clients
        self.view = view

    def CreateView(self, view_idx):
        self.view.Create(self, view_idx)

    def ToggleNewClientMenu(self):
        self.opened_menu = not self.opened_menu
        if self.opened_menu:
            self.view.Show()
        else:
            self.view.Hide()

    def AddNewClient(self, new_client_login):
        new_client = self.new_client_cb(new_client_login)
        if new_client.status is ClientStatus.NEED_OAUTH_CONNECTION:
            self.authenticating_client = new_client
            self.view.ShowOAuthDialog(new_client)
        elif new_client.status is ClientStatus.NEED_PASSWORD:
            self.authenticating_client = new_client
            self.view.ShowPasswordDialog()
        elif new_client.status is ClientStatus.CONNECTED:
            self.AddToConnectedClients(new_client)

    def ConnectClientOAuth(self, oauth_token):
        self.authenticating_client.ConnectOAuth(oauth_token)
        if self.authenticating_client.status is ClientStatus.CONNECTED:
            self.AddToConnectedClients(self.authenticating_client)

    def ConnectClientPassword(self, password):
        self.authenticating_client.Login(self.authenticating_client.GetClientName(), password)
        self.AddToConnectedClients(self.authenticating_client)

    def AddToConnectedClients(self, client):
        self.view.ShowConnectedDialog()
        self.connected_clients.AddClient(client)
