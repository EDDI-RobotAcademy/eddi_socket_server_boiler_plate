from abc import ABC, abstractmethod


class ServerSocketRepository(ABC):
    @abstractmethod
    def create(self):
        pass

    @abstractmethod
    def getServerSocket(self):
        pass

    @abstractmethod
    def reuseSocket(self):
        pass

    @abstractmethod
    def keepAlive(self):
        pass

    @abstractmethod
    def addressBind(self):
        pass

    @abstractmethod
    def howManyListen(self, canListenCount):
        pass

    @abstractmethod
    def setNonBlock(self):
        pass
