import json
import socket
from time import sleep

from acceptor.repository.socket_accept_repository_impl import SocketAcceptRepositoryImpl
from transmitter.repository.transmitter_repository_impl import TransmitterRepositoryImpl
from transmitter.service.transmitter_service import TransmitterService
from utility.color_print import ColorPrinter


class TransmitterServiceImpl(TransmitterService):
    __instance = None

    def __new__(cls):
        if cls.__instance is None:
            cls.__instance = super().__new__(cls)
            cls.__instance.__transmitterRepository = TransmitterRepositoryImpl.getInstance()
            cls.__instance.__socketAcceptRepository = SocketAcceptRepositoryImpl.getInstance()

        return cls.__instance

    @classmethod
    def getInstance(cls):
        if cls.__instance is None:
            cls.__instance = cls()

        return cls.__instance

    # TODO: Change it to Non-Blocking for multiple request
    def validateClientSocket(self):
        ipcAcceptorTransmitterChannel = self.__transmitterRepository.getIpcAcceptorTransmitterChannel()

        while True:
            clientSocket = ipcAcceptorTransmitterChannel.get()
            ColorPrinter.print_important_data("Try to get ClientSocket", f"{clientSocket}")

            if clientSocket is not None:
                return clientSocket

            sleep(0.3)

    def requestToInjectClientSocket(self):
        clientSocket = self.validateClientSocket()
        ColorPrinter.print_important_message("Success to inject client socket to transmitter")

        self.__transmitterRepository.injectClientSocket(clientSocket)

    def requestToInjectAcceptorTransmitterChannel(self, ipcAcceptorTransmitterChannel):
        self.__transmitterRepository.injectAcceptorTransmitterChannel(ipcAcceptorTransmitterChannel)

    # TODO: need to change when operate with FastAPI
    def checkTransmitChannelData(self):
        return "치맥 먹으러 가즈아 ~~!!~!"

    def requestToTransmitClient(self):
        clientSocket = self.__transmitterRepository.getClientSocket()
        clientSocketObject = clientSocket.getClientSocket()

        while True:
            try:
                willTransmitData = self.checkTransmitChannelData()
                ColorPrinter.print_important_data("will transmit data", f"{willTransmitData}")

                serializedTransmitData = json.dumps({"message": willTransmitData}, ensure_ascii=False)
                self.__transmitterRepository.transmit(clientSocketObject, serializedTransmitData)

            except socket.error as socketException:
                if socketException.errno == socket.errno.EAGAIN == socket.errno.EWOULDBLOCK:
                    sleep(0.3)
                else:
                    ColorPrinter.print_important_data("transmitter exception", f"{socketException}")
                    clientSocketObject.close()
                    break

            except Exception as exception:
                ColorPrinter.print_important_data("transmitter exception", f"{exception}")
                clientSocketObject.close()
                break

            finally:
                sleep(0.3)


