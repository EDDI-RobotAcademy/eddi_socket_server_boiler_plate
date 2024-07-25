from abc import ABC, abstractmethod


class SocketAcceptRepository(ABC):
    @abstractmethod
    def injectSocketServer(self, serverSocket):
        pass

    @abstractmethod
    def acceptClient(self):
        pass
