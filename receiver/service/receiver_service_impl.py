import asyncio
import concurrent
import json
import select
import socket
import ssl
import threading
import time
from time import sleep

import requests

from acceptor.repository.socket_accept_repository_impl import SocketAcceptRepositoryImpl
from channel_selector.selector import ChannelSelector
from critical_section.manager import CriticalSectionManager
from http_api.django_http_client import DjangoHttpClient
from lock_manager.socket_lock_manager import SocketLockManager
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

            cls.__instance.__criticalSectionManager = CriticalSectionManager.getInstance()

            cls.__instance.__receiverLock = SocketLockManager.getLock()

        return cls.__instance

    @classmethod
    def getInstance(cls):
        if cls.__instance is None:
            cls.__instance = cls()

        return cls.__instance

    # TODO: Change it to Non-Blocking for multiple request
    def validateClientSocket(self):
        # ipcAcceptorReceiverChannel = self.__receiverRepository.getIpcAcceptorReceiverChannel()

        while True:
            clientSocket = self.__criticalSectionManager.getClientSocket()
            ColorPrinter.print_important_data("Try to get ClientSocket", f"{clientSocket}")

            if clientSocket is not None:
                return clientSocket

            sleep(1)

    def requestToInjectClientSocket(self):
        clientSocket = self.validateClientSocket()
        ColorPrinter.print_important_message("Success to inject client socket to receiver")

        self.__receiverRepository.injectClientSocket(clientSocket)

    def requestToInjectAcceptorReceiverChannel(self, ipcAcceptorReceiverChannel):
        self.__receiverRepository.injectAcceptorReceiverChannel(ipcAcceptorReceiverChannel)

    def requestToInjectReceiverFastAPIChannel(self, ipcReceiverFastAPIChannel):
        self.__receiverRepository.injectReceiverFastAPIChannel(ipcReceiverFastAPIChannel)

    def requestToInjectUserDefinedReceiverFastAPIChannel(self, userDefinedReceiverFastAPIChannel):
        self.__receiverRepository.injectUserDefinedReceiverFastAPIChannel(userDefinedReceiverFastAPIChannel)

    def __recvFixedLength(self, clientSocketObject, length):
        data = b''
        remaining = length

        while remaining > 0:
            try:
                chunk = clientSocketObject.recv(remaining)
                if not chunk:
                    raise ConnectionError("Socket connection lost")
                data += chunk
                remaining -= len(chunk)
            except ssl.SSLWantReadError:
                continue
        return data

    def sendRequestToDjango(self, receivedJson, url):
        with concurrent.futures.ThreadPoolExecutor() as executor:
            future = executor.submit(asyncio.run, DjangoHttpClient.post(url, receivedJson))
            try:
                result = future.result()
            except Exception as e:
                ColorPrinter.print_important_data("Error in sending request to Django", str(e))

    def requestToReceiveClient(self):
        ColorPrinter.print_important_message("Receiver 구동 시작!")

        ipcReceiverFastAPIChannel = self.__receiverRepository.getReceiverFastAPIChannel()
        userDefinedReceiverFastAPIChannel = self.__receiverRepository.getUserDefinedReceiverFastAPIChannel()
        clientSocketObject = None

        while True:
            clientSocket = self.__criticalSectionManager.getClientSocket()
            if clientSocket is None:
                sleep(0.5)
                continue

            clientSocketObject = clientSocket.getClientSocket()
            break

        ColorPrinter.print_important_data("SSL Socket", clientSocketObject)

        while True:
            try:
                ready_to_read, ready_to_write, in_error = select.select([clientSocketObject], [], [], 0.5)

                if not ready_to_read:
                    continue

                with self.__receiverLock:  # threading.Lock을 사용하여 동기화
                    # receivedData = self.__receiverRepository.receive(clientSocketObject)
                    headerData = self.__recvFixedLength(clientSocketObject, 58)
                    ColorPrinter.print_important_data("headerData", headerData)

                    parsedHeaderData = json.loads(headerData)
                    protocolNumber = int(parsedHeaderData.get("protocolNumber"))
                    packetDataLength = int(parsedHeaderData.get("packetDataLength").strip())
                    ColorPrinter.print_important_data("protocolNumber", protocolNumber)
                    ColorPrinter.print_important_data("packetDataLength", packetDataLength)

                    # protocolNumberString = headerData[:8].decode('utf-8').strip()
                    # packetDataLengthString = headerData[8:].decode('utf-8').strip()

                    # protocolNumber = int(protocolNumberString)
                    # packetLength = int(packetDataLengthString)

                    # 지정된 길이만큼 데이터 수신
                    receivedData = self.__recvFixedLength(clientSocketObject, packetDataLength)

                if not receivedData:
                    clientSocketObject.close()
                    break

                decodedReceiveData = receivedData.decode()
                ColorPrinter.print_important_data("수신 정보", f"{decodedReceiveData}")

                receivedJson = json.loads(decodedReceiveData)
                if receivedJson.get("tag") == "conditional-custom-executor":
                    tagUrl = receivedJson.get("tag")
                    thread = threading.Thread(target=self.sendRequestToDjango, args=(receivedJson, tagUrl,))
                    thread.start()

                    continue

                # TODO: 사실 좀 더 개선하는 것이 좋음 (추후 확장성을 고려한다면)
                isItUserDefinedChannel = ChannelSelector.findUserDefinedReceiverChannel(decodedReceiveData)
                if isItUserDefinedChannel is True:
                    ColorPrinter.print_important_message("UserDefined 정보 Receiver Channel에 데이터 설정")
                    if userDefinedReceiverFastAPIChannel is not None:
                        userDefinedReceiverFastAPIChannel.put(decodedReceiveData)
                else:
                    ColorPrinter.print_important_message("FastAPI Receiver Channel에 데이터 설정")
                    if ipcReceiverFastAPIChannel is not None:
                        ipcReceiverFastAPIChannel.put(decodedReceiveData)

            except ssl.SSLError as ssl_error:
                ColorPrinter.print_important_data("SSL error during receive", str(ssl_error))
                clientSocketObject.close()

            except socket.error as socketException:
                if socketException.errno == socket.errno.EAGAIN == socket.errno.EWOULDBLOCK:
                    continue
                else:
                    ColorPrinter.print_important_data("receiver exception", f"{socketException}")
                    clientSocketObject.close()

            except Exception as exception:
                ColorPrinter.print_important_data("receiver exception", f"{exception}")
                clientSocketObject.close()

            finally:
                sleep(0.5)
