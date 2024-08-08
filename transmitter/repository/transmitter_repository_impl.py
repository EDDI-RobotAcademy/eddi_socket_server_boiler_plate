from transmitter.repository.transmitter_repository import TransmitterRepository


class TransmitterRepositoryImpl(TransmitterRepository):
    __instance = None
    __clientSocket = None

    __ipcAcceptorTransmitterChannel = None

    # FastAPI와 Socket Server의 Transmitter를 연결하는 채널
    __ipcFastAPITransmitterChannel = None

    def __new__(cls):
        if cls.__instance is None:
            cls.__instance = super().__new__(cls)

        return cls.__instance

    @classmethod
    def getInstance(cls):
        if cls.__instance is None:
            cls.__instance = cls()

        return cls.__instance

    def getIpcAcceptorTransmitterChannel(self):
        return self.__ipcAcceptorTransmitterChannel

    def getClientSocket(self):
        return self.__clientSocket

    def injectClientSocket(self, clientSocket):
        self.__clientSocket = clientSocket

    def injectAcceptorTransmitterChannel(self, ipcAcceptorTransmitterChannel):
        self.__ipcAcceptorTransmitterChannel = ipcAcceptorTransmitterChannel

    def injectFastAPITransmitterChannel(self, ipcFastAPITransmitterChannel):
        self.__ipcFastAPITransmitterChannel = ipcFastAPITransmitterChannel

    def getIpcFastAPITransmitterChannel(self):
        return self.__ipcFastAPITransmitterChannel

    def transmit(self, clientSocketObject, serializedTransmitData):
        clientSocketObject.sendall(serializedTransmitData.encode())
