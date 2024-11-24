import tkinter as tk
from tkinter import END
import webbrowser


class MastodonView(object):
    def __init__(self, parent):
        self.parent = parent

    def Create(self, controller):
        self.titleButton = tk.Button(self.parent, text="Mastodon", command=controller.ToggleNewClientMenu).grid(row=1, column=2, pady=10)
        self.masto_client_id_prompt = tk.Label(self.parent, text="Mastodon Client identifier:")
        self.masto_client_id_entry = tk.Entry(self.parent)
        self.masto_client_id_entry.insert(END, 'e.g. @Toot@mastodon.social')

        def AddNewClientCallback(): controller.AddNewClient(self.masto_client_id_entry.get())
        connect_callback = AddNewClientCallback
        self.connect_masto_btn = tk.Button(self.parent, text="Connect", command=connect_callback)

        self.oauth_token_prompt = tk.Label(self.parent, text="OAuth Token:")
        self.oauth_token_entry = tk.Entry(self.parent)

        def ConnectClientOAuthCallback(): controller.ConnectClientOAuth(oauth_token=self.oauth_token_entry.get())
        submit_oauth_callback = ConnectClientOAuthCallback
        self.submit_token_btn = tk.Button(self.parent, text="Submit", command=submit_oauth_callback)

        self.oauth_result = tk.Label(self.parent, text="Connection successful!", fg="green")

    def Show(self):
        self.masto_client_id_prompt.grid(row=2, column=3)
        self.masto_client_id_entry.grid(row=2, column=4)
        self.connect_masto_btn.grid(row=2, column=5)

    def Hide(self):
        self.masto_client_id_prompt.grid_forget()
        self.masto_client_id_entry.grid_forget()
        self.connect_masto_btn.grid_forget()
        self.oauth_token_prompt.grid_forget()
        self.oauth_token_entry.grid_forget()
        self.submit_token_btn.grid_forget()
        self.oauth_result.grid_forget()

    def ShowOAuthDialog(self, authenticating_client):
        oauth_url = authenticating_client.GetOAuthURL()
        webbrowser.open(oauth_url)
        self.oauth_token_prompt.grid(row=3, column=3)
        self.oauth_token_entry.grid(row=3, column=4)
        self.submit_token_btn.grid(row=3, column=5)

    def ShowConnectedDialog(self):
        self.oauth_result.grid(row=4, column=4)
