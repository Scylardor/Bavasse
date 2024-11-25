import tkinter as tk
from tkinter import END


class BlueskyView(object):
    def __init__(self, parent):
        self.parent = parent

    def Create(self, controller, view_idx):
        self.titleButton = tk.Button(self.parent, text="Bluesky", command=controller.ToggleNewClientMenu).grid(row=1 + view_idx, column=2, pady=10)
        self.bluesky_client_id_prompt = tk.Label(self.parent, text="Bluesky Handle (without @):")
        self.bluesky_client_id_entry = tk.Entry(self.parent)
        self.bluesky_client_id_entry.insert(END, 'e.g. JohnDoe.bsky.social')

        def AddNewClientCallback():
            controller.AddNewClient(self.bluesky_client_id_entry.get())
        connect_callback = AddNewClientCallback
        self.connect_bs_btn = tk.Button(self.parent, text="Connect", command=connect_callback)

        self.password_prompt = tk.Label(self.parent, text="App Password (not user):")
        self.password_entry = tk.Entry(self.parent, show="*", width=15)

        def ConnectClientPasswordCallback():
            controller.ConnectClientPassword(password=self.password_entry.get())
        submit_password_callback = ConnectClientPasswordCallback
        self.submit_password_btn = tk.Button(self.parent, text="Submit", command=submit_password_callback)

        self.password_result = tk.Label(self.parent, text="Connection successful!", fg="green")

    def Show(self):
        self.bluesky_client_id_prompt.grid(row=2, column=3)
        self.bluesky_client_id_entry.grid(row=2, column=4)
        self.connect_bs_btn.grid(row=2, column=5)

    def Hide(self):
        self.bluesky_client_id_prompt.grid_forget()
        self.bluesky_client_id_entry.grid_forget()
        self.connect_bs_btn.grid_forget()
        self.password_prompt.grid_forget()
        self.password_entry.grid_forget()
        self.submit_password_btn.grid_forget()
        self.password_result.grid_forget()

    def ShowPasswordDialog(self):
        self.password_prompt.grid(row=3, column=3)
        self.password_entry.grid(row=3, column=4)
        self.submit_password_btn.grid(row=3, column=5)

    def ShowConnectedDialog(self):
        self.password_result.grid(row=4, column=4)
