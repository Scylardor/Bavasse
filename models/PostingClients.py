class PostingClients(object):
    def __init__(self, client_nbr):
        self.client_indexes = list(range(client_nbr))

    def __iter__(self):
        return iter(self.client_indexes)  # Use the iterator of the internal iterable

    def AddPostingClient(self, client_idx):
        self.client_indexes.append(client_idx)

    def RemovePostingClient(self, client_idx):
        self.client_indexes.remove(client_idx)
