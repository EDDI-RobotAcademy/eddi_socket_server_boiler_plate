import socket
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

    # TODO: Change it to Non-Blocking for multiple request
    def validateClientSocket(self):
        ipcAcceptorReceiverChannel = self.__receiverRepository.getIpcAcceptorReceiverChannel()

        while True:
            clientSocket = ipcAcceptorReceiverChannel.get()
            ColorPrinter.print_important_data("Try to get ClientSocket", f"{clientSocket}")

            if clientSocket is not None:
                return clientSocket

            sleep(0.3)

    def requestToInjectClientSocket(self):
        clientSocket = self.validateClientSocket()
        ColorPrinter.print_important_message("Success to inject client socket to receiver")

        self.__receiverRepository.injectClientSocket(clientSocket)

    def requestToInjectAcceptorReceiverChannel(self, ipcAcceptorReceiverChannel):
        self.__receiverRepository.injectAcceptorReceiverChannel(ipcAcceptorReceiverChannel)

    def requestToInjectReceiverFastAPIChannel(self, ipcReceiverFastAPIChannel):
        self.__receiverRepository.injectReceiverFastAPIChannel(ipcReceiverFastAPIChannel)

    def requestToReceiveClient(self):
        ColorPrinter.print_important_message("Receiver 구동 시작!")
        clientSocket = self.__receiverRepository.getClientSocket()
        clientSocketObject = clientSocket.getClientSocket()

        while True:
            try:
                receivedData = self.__receiverRepository.receive(clientSocketObject)
                if not receivedData:
                    clientSocketObject.close()
                    break

                decodedReceiveData = receivedData.decode()
                ColorPrinter.print_important_data("수신 정보", f"{decodedReceiveData}")

            except socket.error as socketException:
                if socketException.errno == socket.errno.EAGAIN == socket.errno.EWOULDBLOCK:
                    sleep(0.3)
                else:
                    ColorPrinter.print_important_data("receiver exception", f"{socketException}")
                    clientSocketObject.close()
                    break

            except Exception as exception:
                ColorPrinter.print_important_data("receiver exception", f"{exception}")
                clientSocketObject.close()
                break

            finally:
                sleep(0.3)
