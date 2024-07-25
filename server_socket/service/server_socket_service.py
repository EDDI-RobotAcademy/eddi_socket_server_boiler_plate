from abc import ABC, abstractmethod


class ServerSocketService(ABC):
    @abstractmethod
    def prepareServerSocket(self):
        pass
