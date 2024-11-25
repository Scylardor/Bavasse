import tkinter as tk

from clients import MastodonClient, BlueskyClient
from models import ConnectedClients, PostingClients
from views import BavasseView

from pathlib import Path


class App(tk.Tk):
    def __init__(self):
        super(App, self).__init__()

        self.geometry('500x500')

        self.name = 'Bavasse'
        self.savedata_folder = Path('bavasse_data')

        self.connected_clients = ConnectedClients([MastodonClient.LookupExistingClients, BlueskyClient.LookupExistingClients], self.name, self.savedata_folder)
        self.posting_clients = PostingClients(len(self.connected_clients.clients))

        self.main_view = BavasseView(self)


def main():
    app = App()
    app.mainloop()


if __name__ == '__main__':
    main()
