from .CollapsiblePane import CollapsiblePane
from .MastodonView import MastodonView
from controllers import NewClientController
from clients import MastodonClient


class NewClientView(object):
    def __init__(self, parent):
        self.pane = CollapsiblePane(parent, 'Hide new social network client menu', 'Add new social network client')
        self.vcs = [self.GetMastodonViewController(parent)]

    def GetMastodonViewController(self, parent):
        def CreateNewMastodonClient(login_id):
            return MastodonClient(parent.name, login_id, parent.savedata_folder / "mastodon")

        masto_new_client_cb = CreateNewMastodonClient
        masto_view = MastodonView(self.pane.frame)
        masto_vc = (masto_view, NewClientController(masto_view, masto_new_client_cb, parent.connected_clients))
        return masto_vc
