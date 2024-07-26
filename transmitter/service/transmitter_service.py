from abc import ABC, abstractmethod


class TransmitterService(ABC):
    @abstractmethod
    def requestToInjectClientSocket(self):
        pass

    @abstractmethod
    def requestToTransmitClient(self):
        pass
