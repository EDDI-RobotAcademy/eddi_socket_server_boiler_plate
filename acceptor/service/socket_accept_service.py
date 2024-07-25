from abc import ABC, abstractmethod


class SocketAcceptService(ABC):
    @abstractmethod
    def requestToInjectServerSocket(self, serverSocket):
        pass

    @abstractmethod
    def requestToAcceptClient(self):
        pass
