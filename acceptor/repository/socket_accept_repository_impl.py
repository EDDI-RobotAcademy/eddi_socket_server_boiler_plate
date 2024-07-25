from acceptor.repository.socket_accept_repository import SocketAcceptRepository


class SocketAcceptRepositoryImpl(SocketAcceptRepository):
    __instance = None
    __serverSocket = None

    def __new__(cls):
        if cls.__instance is None:
            cls.__instance = super().__new__(cls)

        return cls.__instance

    @classmethod
    def getInstance(cls):
        if cls.__instance is None:
            cls.__instance = cls()

        return cls.__instance

    def injectSocketServer(self, serverSocket):
        self.__serverSocket = serverSocket