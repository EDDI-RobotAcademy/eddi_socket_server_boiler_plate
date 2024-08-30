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

from template.include.socket_server.request_generator.packet_length_request import PacketLengthRequest


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

    def __transmitInChunks(self, clientSocketObject, data, chunkSize=4096):
        total_length = len(data)
        sent_length = 0

        while sent_length < total_length:
            chunk = data[sent_length:sent_length + chunkSize]
            clientSocketObject.sendall(chunk.encode('utf-8'))
            sent_length += len(chunk)
            ColorPrinter.print_important_data("송신한 청크 길이", len(chunk))

        ColorPrinter.print_important_message("모든 청크 전송 완료")

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
                if ipcFastAPITransmitterChannel is not None:
                    requestCommandData = ipcFastAPITransmitterChannel.get()
                else:
                    commandData = {
                        "command": count % 2 + 1,
                        "data": None
                    }
                    requestCommandData = json.dumps(commandData)
                    count += 1

                utf8EncodedRequestCommandData = requestCommandData.encode('utf-8')
                ColorPrinter.print_important_data("송신 할 정보", f"{utf8EncodedRequestCommandData}")

                packetLength = len(utf8EncodedRequestCommandData)
                nonEncodedRequestCommandData = len(requestCommandData)
                ColorPrinter.print_important_data("인코딩하지 않은 패킷 길이", nonEncodedRequestCommandData)
                ColorPrinter.print_important_data("전체 패킷 길이", packetLength)

                # 일관성 유지를 위해 PacketLengthResponse를 구성하도록 만든다.
                packetLengthRequest = PacketLengthRequest(packetLength)
                dictionarizedPacketLengthResponse = packetLengthRequest.toFixedSizeDictionary()
                serializedPacketLengthData = json.dumps(dictionarizedPacketLengthResponse, ensure_ascii=False)

                with self.__transmitterLock:
                    self.__transmitterRepository.transmit(clientSocketObject, serializedPacketLengthData)
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


