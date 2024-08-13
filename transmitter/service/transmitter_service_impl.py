import json
import socket
import threading
from time import sleep

from acceptor.repository.socket_accept_repository_impl import SocketAcceptRepositoryImpl
from critical_section.manager import CriticalSectionManager
from default_protocol.entity.default_protocol import DefaultProtocolNumber
from lock_manager.socket_lock_manager import SocketLockManager
from request_generator.generator import RequestGenerator
from request_generator.request_type import RequestType
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

            cls.__instance.__criticalSectionManager = CriticalSectionManager.getInstance()

            cls.__instance.__transmitterLock = SocketLockManager.getLock()

        return cls.__instance

    @classmethod
    def getInstance(cls):
        if cls.__instance is None:
            cls.__instance = cls()

        return cls.__instance

    # TODO: Change it to Non-Blocking for multiple request
    def validateClientSocket(self):
        while True:
            clientSocket = self.__criticalSectionManager.getClientSocket()
            ColorPrinter.print_important_data("Try to get ClientSocket", f"{clientSocket}")

            if clientSocket is not None:
                return clientSocket

            sleep(1)

    def requestToInjectClientSocket(self):
        clientSocket = self.validateClientSocket()
        ColorPrinter.print_important_message("Success to inject client socket to transmitter")

        self.__transmitterRepository.injectClientSocket(clientSocket)

    def requestToInjectAcceptorTransmitterChannel(self, ipcAcceptorTransmitterChannel):
        self.__transmitterRepository.injectAcceptorTransmitterChannel(ipcAcceptorTransmitterChannel)

    def requestToInjectFastAPITransmitterChannel(self, ipcFastAPITransmitterChannel):
        self.__transmitterRepository.injectFastAPITransmitterChannel(ipcFastAPITransmitterChannel)

    # TODO: need to change when operate with FastAPI
    def checkTransmitChannelData(self):
        rollDiceRequest = RequestGenerator.generate(DefaultProtocolNumber.ROLL_DICE)
        return rollDiceRequest.toDictionary()

    def requestToTransmitClient(self):
        ColorPrinter.print_important_message("Transmitter 구동 시작!")

        ipcFastAPITransmitterChannel = self.__transmitterRepository.getIpcFastAPITransmitterChannel()
        clientSocketObject = None

        while True:
            clientSocket = self.__criticalSectionManager.getClientSocket()
            if clientSocket is None:
                sleep(0.5)
                continue

            clientSocketObject = clientSocket.getClientSocket()
            break

        count = 0

        while True:
            try:
                with self.__transmitterLock:
                    if ipcFastAPITransmitterChannel is not None:
                        requestCommandData = ipcFastAPITransmitterChannel.get()
                    else:
                        commandData = {
                            "command": count % 2 + 1,
                            "data": None
                        }
                        requestCommandData = json.dumps(commandData)
                        count += 1

                    ColorPrinter.print_important_data("송신 할 정보", f"{requestCommandData}")

                    self.__transmitterRepository.transmit(clientSocketObject, requestCommandData)

            except socket.error as socketException:
                if socketException.errno == socket.errno.EAGAIN == socket.errno.EWOULDBLOCK:
                    sleep(0.5)
                else:
                    ColorPrinter.print_important_data("transmitter exception", f"{socketException}")
                    clientSocketObject.close()
                    break

            except Exception as exception:
                ColorPrinter.print_important_data("transmitter exception", f"{exception}")
                clientSocketObject.close()
                break

            finally:
                sleep(0.5)


