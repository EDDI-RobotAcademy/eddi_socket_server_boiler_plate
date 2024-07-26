import multiprocessing

from ipc_queue.repository.ipc_queue_repository import IPCQueueRepository


class IPCQueueRepositoryImpl(IPCQueueRepository):
    __instance = None

    __ipcAcceptorReceiverChannel = None
    __ipcAcceptorTransmitterChannel = None

    def __new__(cls):
        if cls.__instance is None:
            cls.__instance = super().__new__(cls)

        return cls.__instance

    @classmethod
    def getInstance(cls):
        if cls.__instance is None:
            cls.__instance = cls()

        return cls.__instance

    def getIPCAcceptorReceiverChannel(self):
        return self.__ipcAcceptorReceiverChannel

    def getIPCAcceptorTransmitterChannel(self):
        return self.__ipcAcceptorTransmitterChannel

    def createDefault(self):
        self.__ipcAcceptorReceiverChannel = multiprocessing.Queue()
        self.__ipcAcceptorTransmitterChannel = multiprocessing.Queue()
    