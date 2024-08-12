import threading


class SocketLockManager:
    __lock = threading.Lock()

    @classmethod
    def getLock(cls):
        return cls.__lock
