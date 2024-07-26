from abc import ABC, abstractmethod


class IPCQueueRepository(ABC):
    @abstractmethod
    def createDefault(self):
        pass
