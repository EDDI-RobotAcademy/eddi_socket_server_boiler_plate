from acceptor.repository.socket_accept_repository_impl import SocketAcceptRepositoryImpl
from acceptor.service.socket_accept_service import SocketAcceptService


class SocketAcceptServiceImpl(SocketAcceptService):
    __instance = None

    def __new__(cls):
        if cls.__instance is None:
            cls.__instance = super().__new__(cls)
            cls.__instance.__socketAcceptRepository = SocketAcceptRepositoryImpl.getInstance()

        return cls.__instance

    @classmethod
    def getInstance(cls):
        if cls.__instance is None:
            cls.__instance = cls()

        return cls.__instance

    def requestToInjectServerSocket(self, serverSocket):
        self.__socketAcceptRepository.injectSocketServer(serverSocket)

    def requestToAcceptClient(self):
        self.__socketAcceptRepository.acceptClient()

    # def requestToInjectAcceptorReceiverChannel(self, ipcAcceptorReceiverChannel):
    #     self.__socketAcceptRepository.injectAcceptorReceiverChannel(ipcAcceptorReceiverChannel)

    # def requestToInjectAcceptorTransmitterChannel(self, ipcAcceptorTransmitterChannel):
    #     self.__socketAcceptRepository.injectAcceptorTransmitterChannel(ipcAcceptorTransmitterChannel)
    