from .CollapsiblePane import CollapsiblePane
from .MastodonView import MastodonView
from .BlueskyView import BlueskyView
from controllers import NewClientController
from clients import MastodonClient, BlueskyClient


class NewClientView(object):
    def __init__(self, parent):
        self.pane = CollapsiblePane(parent, 'Hide new social network client menu', 'Add new social network client')
        self.vcs = [self.GetMastodonViewController(parent), self.GetBlueskyViewController(parent)]
        for i, (view, controller) in enumerate(self.vcs):
            controller.CreateView(i)

    def GetMastodonViewController(self, parent):
        def CreateNewMastodonClient(login_id):
            return MastodonClient(parent.name, login_id, parent.savedata_folder / "mastodon")

        masto_new_client_cb = CreateNewMastodonClient
        masto_view = MastodonView(self.pane.frame)
        masto_vc = (masto_view, NewClientController(masto_view, masto_new_client_cb, parent.connected_clients))
        return masto_vc

    def GetBlueskyViewController(self, parent):
        def CreateNewBlueskyClient(login_id):
            return BlueskyClient(parent.name, parent.savedata_folder, user_name=login_id)

        bs_new_client_cb = CreateNewBlueskyClient
        bs_view = BlueskyView(self.pane.frame)
        bs_vc = (bs_view, NewClientController(bs_view, bs_new_client_cb, parent.connected_clients))
        return bs_vc
