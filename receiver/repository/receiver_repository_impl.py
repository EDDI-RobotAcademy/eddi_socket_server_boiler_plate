from receiver.repository.receiver_repository import ReceiverRepository


class ReceiverRepositoryImpl(ReceiverRepository):
    __instance = None
    __clientSocket = None

    __ipcAcceptorReceiverChannel = None

    # FastAPI와 Socket Server의 Receiver를 연결하는 채널
    __ipcReceiverFastAPIChannel = None

    # DLLS-FastAPI와 Socket Server의 Receiver를 연결하는 채널
    __userDefinedReceiverFastAPIChannel = None

    NETWORK_BUFFER_SIZE = 2048

    def __new__(cls):
        if cls.__instance is None:
            cls.__instance = super().__new__(cls)

        return cls.__instance

    @classmethod
    def getInstance(cls):
        if cls.__instance is None:
            cls.__instance = cls()

        return cls.__instance

    def getIpcAcceptorReceiverChannel(self):
        return self.__ipcAcceptorReceiverChannel

    def getClientSocket(self):
        return self.__clientSocket

    def injectClientSocket(self, clientSocket):
        self.__clientSocket = clientSocket

    def injectAcceptorReceiverChannel(self, ipcAcceptorReceiverChannel):
        self.__ipcAcceptorReceiverChannel = ipcAcceptorReceiverChannel

    def injectReceiverFastAPIChannel(self, ipcReceiverFastAPIChannel):
        self.__ipcReceiverFastAPIChannel = ipcReceiverFastAPIChannel

    def injectUserDefinedReceiverFastAPIChannel(self, userDefinedReceiverFastAPIChannel):
        self.__userDefinedReceiverFastAPIChannel = userDefinedReceiverFastAPIChannel

    def getReceiverFastAPIChannel(self):
        return self.__ipcReceiverFastAPIChannel

    def getUserDefinedReceiverFastAPIChannel(self):
        return self.__userDefinedReceiverFastAPIChannel

    def receive(self, clientSocketObject):
        receivedData = clientSocketObject.recv(self.NETWORK_BUFFER_SIZE)
        return receivedData
