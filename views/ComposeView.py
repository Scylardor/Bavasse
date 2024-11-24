import tkinter as tk
from .CollapsiblePane import CollapsiblePane


class ComposeView(object):
    def __init__(self, parent):
        self.pane = CollapsiblePane(parent, 'Hide compose menu', 'Compose')
        self.parent = parent

        self.compose_text = tk.Text(self.pane.frame)
        self.compose_text.grid(row=0, column=0, pady=0)
        self.compose_text.bind("<<Modified>>", self.OnTextChange)

    def OnTextChange(self, event):
        self.parent.message = self.compose_text.get("1.0", tk.END)
        # Reset the modified flag to prevent recursive triggering
        self.compose_text.edit_modified(False)
