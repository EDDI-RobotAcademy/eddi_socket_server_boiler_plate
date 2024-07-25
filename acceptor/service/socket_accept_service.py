from abc import ABC, abstractmethod


class SocketAcceptService(ABC):
    @abstractmethod
    def requestToInjectSocketServer(self, serverSocket):
        pass
