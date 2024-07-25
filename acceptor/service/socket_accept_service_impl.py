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

    def requestToInjectSocketServer(self, serverSocket):
        self.__socketAcceptRepository.injectSocketServer(serverSocket)
    