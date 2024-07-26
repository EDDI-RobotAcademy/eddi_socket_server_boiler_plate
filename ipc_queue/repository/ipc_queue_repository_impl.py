import multiprocessing

from ipc_queue.repository.ipc_queue_repository import IPCQueueRepository


class IPCQueueRepositoryImpl(IPCQueueRepository):
    __instance = None

    __ipcAcceptorChannel = None

    def __new__(cls):
        if cls.__instance is None:
            cls.__instance = super().__new__(cls)

        return cls.__instance

    @classmethod
    def getInstance(cls):
        if cls.__instance is None:
            cls.__instance = cls()

        return cls.__instance

    def getIPCAcceptorChannel(self):
        return self.__ipcAcceptorChannel

    def createDefault(self):
        self.__ipcAcceptorChannel = multiprocessing.Queue()
    