from abc import ABC, abstractmethod


class ReceiverService(ABC):
    @abstractmethod
    def createReceiver(self):
        pass
