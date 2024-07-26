from time import sleep

from acceptor.repository.socket_accept_repository_impl import SocketAcceptRepositoryImpl
from receiver.repository.receiver_repository_impl import ReceiverRepositoryImpl
from receiver.service.receiver_service import ReceiverService
from utility.color_print import ColorPrinter


class ReceiverServiceImpl(ReceiverService):
    __instance = None

    def __new__(cls):
        if cls.__instance is None:
            cls.__instance = super().__new__(cls)
            cls.__instance.__receiverRepository = ReceiverRepositoryImpl.getInstance()
            cls.__instance.__socketAcceptRepository = SocketAcceptRepositoryImpl.getInstance()

        return cls.__instance

    @classmethod
    def getInstance(cls):
        if cls.__instance is None:
            cls.__instance = cls()

        return cls.__instance

    def validateClientSocket(self):
        ipcAcceptorChannel = self.__receiverRepository.getIpcAcceptorChannel

        while True:
            clientSocket = ipcAcceptorChannel.get()
            ColorPrinter.print_important_data("Try to get ClientSocket", f"{clientSocket}")

            if clientSocket is not None:
                return clientSocket

            sleep(0.3)

    def requestToInjectClientSocket(self):
        clientSocket = self.validateClientSocket()
        ColorPrinter.print_important_message("Success to inject client socket to receiver")

        self.__receiverRepository.injectClientSocket(clientSocket)

    def requestToInjectAcceptChannel(self, ipcAcceptorChannel):
        self.__receiverRepository.injectAcceptChannel(ipcAcceptorChannel)
