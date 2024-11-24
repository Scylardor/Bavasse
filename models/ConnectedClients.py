class ConnectedClients(object):
    def __init__(self, client_lookup_funcs, app_name, app_data_folder):
        self.clients = []
        for f in client_lookup_funcs:
            self.clients.extend(f(app_name, app_data_folder))

    def __iter__(self):
        return iter(self.clients)  # Use the iterator of the internal iterable

    def AddClient(self, client):
        self.clients.append(client)

    def RemoveClient(self, client):
        self.clients.remove(client)
