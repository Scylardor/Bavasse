class PostController(object):
    def __init__(self, view, app):
        self.view = view
        self.connected_clients = app.connected_clients
        self.posting_clients = app.posting_clients
        self.app = app
        view.Create(self)
        self.UpdateClientList()

    def UpdateClientList(self):
        client_states = []
        for index, client in enumerate(self.connected_clients):
            client_states.append((client.GetClientName(), index in self.posting_clients))
        self.view.UpdateClientsState(client_states)

    def ToggleClientPosting(self, client_idx, is_posting):
        if is_posting:
            self.posting_clients.AddPostingClient(client_idx)
        else:
            self.posting_clients.RemovePostingClient(client_idx)

    def TriggerPosting(self):
        for idx in self.posting_clients:
            self.connected_clients.clients[idx].Post(self.app.message)
        self.view.ShowPostSuccessful()
