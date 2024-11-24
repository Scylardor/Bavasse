from .NewClientView import NewClientView
from .ComposeView import ComposeView
from .PostView import PostView
from controllers import PostController


class BavasseView(object):
    def __init__(self, parent):
        self.new_client_view = NewClientView(parent)
        self.new_client_view.pane.grid(row=0, column=0)

        self.compose_view = ComposeView(parent)
        self.compose_view.pane.grid(row=1, column=0)

        self.post_view = PostView(parent)
        self.post_view.pane.grid(row=2, column=0)
        self.post_controller = PostController(self.post_view, parent)
