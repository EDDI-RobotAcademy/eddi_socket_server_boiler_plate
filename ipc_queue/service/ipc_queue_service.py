from abc import ABC, abstractmethod


class IPCQueueService(ABC):
    @abstractmethod
    def createDefaultIPCQueue(self):
        pass
