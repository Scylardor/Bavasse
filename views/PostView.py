import tkinter as tk
from .CollapsiblePane import CollapsiblePane


class PostView(object):
    def __init__(self, parent):
        self.parent = parent
        self.pane = CollapsiblePane(self.parent, 'Hide post menu', 'Post')

    def Create(self, controller):
        self.controller = controller

        self.post_list_label = tk.Label(self.pane.frame, text="Choose which clients should post:").grid(row=0, column=0, pady=0)
        self.post_btn = tk.Button(self.pane.frame, text="Post to Selected Clients", command=controller.TriggerPosting)
        self.post_status = tk.Label(self.pane.frame, text="Post successful!", fg="green")
        self.checkboxes = []

    def UpdateClientsState(self, client_states):
        # forget everything
        for checkbox in self.checkboxes:
            checkbox.grid_forget()
        self.checkboxes = []

        for i, (client_name, is_posting) in enumerate(client_states):
            checkbox_var = tk.BooleanVar(value=is_posting)  # Variable to track the state of the checkbox
            checkbox = tk.Checkbutton(
                self.pane.frame,
                text=client_name,
                variable=checkbox_var,
                command=lambda i=i, var=checkbox_var: self.controller.ToggleClientPosting(i, var.get())
            )
            checkbox.grid(row=i + 1, column=0, pady=0)
            self.checkboxes.append(checkbox_var)  # Add the variable to the list

        # Reposition the post buttons
        self.post_btn.grid_forget()
        self.post_btn.grid(row=len(self.checkboxes) + 2, column=0, pady=0)
        self.post_status.grid_forget()

    def ShowPostSuccessful(self):
        self.post_status.grid(row=len(self.checkboxes) + 3, column=0, pady=0)
