import select
import socket
import ssl
import threading
from time import sleep

from acceptor.repository.socket_accept_repository_impl import SocketAcceptRepositoryImpl
from critical_section.manager import CriticalSectionManager
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

    def requestToReceiveClient(self):
        ColorPrinter.print_important_message("Receiver 구동 시작!")

        ipcReceiverFastAPIChannel = self.__receiverRepository.getReceiverFastAPIChannel()
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
                with self.__receiverLock:  # threading.Lock을 사용하여 동기화
                    ready_to_read, ready_to_write, in_error = select.select([clientSocketObject], [], [], 0.5)

                    if not ready_to_read:
                        continue

                    receivedData = self.__receiverRepository.receive(clientSocketObject)

                if not receivedData:
                    clientSocketObject.close()
                    break

                decodedReceiveData = receivedData.decode()
                ColorPrinter.print_important_data("수신 정보", f"{decodedReceiveData}")

                # TODO: 아마도 나중에 여기서 어떤 정보들을 요청하느냐에 따라 추가적인 관리가 필요할 것임
                # 이제 여기서 FastAPI가 결과를 유지하고 있도록 Queue에 저장해둡니다.
                if ipcReceiverFastAPIChannel is not None:
                    ipcReceiverFastAPIChannel.put(decodedReceiveData)

            except ssl.SSLError as ssl_error:
                ColorPrinter.print_important_data("SSL error during receive", str(ssl_error))
                clientSocketObject.close()

            except socket.error as socketException:
                if socketException.errno == socket.errno.EAGAIN == socket.errno.EWOULDBLOCK:
                    sleep(0.3)
                else:
                    ColorPrinter.print_important_data("receiver exception", f"{socketException}")
                    clientSocketObject.close()

            except Exception as exception:
                ColorPrinter.print_important_data("receiver exception", f"{exception}")
                clientSocketObject.close()

            finally:
                sleep(0.3)
