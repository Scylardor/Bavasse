from enum import Enum


class ClientStatus(Enum):
    DISCONNECTED = 0
    CONNECTED = 1
    NEED_OAUTH_CONNECTION = 2
    NEED_PASSWORD = 3
