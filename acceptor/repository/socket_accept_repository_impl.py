import multiprocessing
import socket
import ssl
from time import sleep

from acceptor.entity.accepted_client_socket import AcceptedClientSocket
from acceptor.repository.socket_accept_repository import SocketAcceptRepository
from critical_section.manager import CriticalSectionManager
from ssl_tls.ssl_tls_context_manager import SslTlsContextManager
from utility.color_print import ColorPrinter


class SocketAcceptRepositoryImpl(SocketAcceptRepository):
    __instance = None

    __serverSocket = None
    __clientSocket = None

    __ipcAcceptorReceiverChannel = None
    __ipcAcceptorTransmitterChannel = None

    def __new__(cls):
        if cls.__instance is None:
            cls.__instance = super().__new__(cls)

        return cls.__instance

    @classmethod
    def getInstance(cls):
        if cls.__instance is None:
            cls.__instance = cls()

        return cls.__instance

    def getClientSocket(self):
        critical_section_manager = CriticalSectionManager.getInstance()
        clientSocket = critical_section_manager.getClientSocket()
        ColorPrinter.print_important_data("accept repository -> getClientSocket()", f"{clientSocket}")
        return clientSocket

    def killAllTask(self):
        for activeTask in multiprocessing.active_children():
            ColorPrinter.print_important_data("Terminated Task", f"{activeTask.pid}")
            activeTask.terminate()
            activeTask.join()

    def injectSocketServer(self, serverSocket):
        self.__serverSocket = serverSocket

    def injectAcceptorReceiverChannel(self, ipcAcceptorReceiverChannel):
        self.__ipcAcceptorReceiverChannel = ipcAcceptorReceiverChannel

    def injectAcceptorTransmitterChannel(self, ipcAcceptorTransmitterChannel):
        self.__ipcAcceptorTransmitterChannel = ipcAcceptorTransmitterChannel

    def acceptClient(self):
        serverSocketObject = self.__serverSocket.getServerSocket()
        SslTlsContextManager.initSslTlsContext()
        sslContext = SslTlsContextManager.getSSLContext()
        critical_section_manager = CriticalSectionManager.getInstance()

        while True:
            try:
                clientSocket, clientAddress = serverSocketObject.accept()
                ColorPrinter.print_important_data("Accepted connection", clientAddress)

                clientSocket.settimeout(5)

                try:
                    sslClientSocket = sslContext.wrap_socket(clientSocket, server_side=True)
                    ColorPrinter.print_important_data("SSL handshake successful", clientAddress)

                    sslClientSocket.setblocking(False)
                    acceptedClientSocket = AcceptedClientSocket(sslClientSocket, clientAddress)
                    critical_section_manager.setClientSocket(acceptedClientSocket)

                    ColorPrinter.print_important_data("Success to accept client socket", f"{sslClientSocket}")

                except ssl.SSLError as ssl_error:
                    ColorPrinter.print_important_data("(인증되지 않은 사용자) Failed to establish SSL connection",
                                                      str(ssl_error))
                    clientSocket.close()

                except socket.timeout:
                    ColorPrinter.print_important_data("(인증되지 않은 사용자) SSL handshake timed out", clientAddress)
                    clientSocket.close()

            except KeyboardInterrupt:
                print('server stopped')
                self.killAllTask()

            except socket.error:
                sleep(0.5)

            except Exception as e:
                self.killAllTask()

        # while True:
        #     try:
        #         clientSocket, clientAddress = serverSocketObject.accept()
        #         clientSocket.setblocking(False)
        #
        #         self.__clientSocket = AcceptedClientSocket(clientSocket, clientAddress)
        #         self.__ipcAcceptorReceiverChannel.put(self.__clientSocket)
        #         self.__ipcAcceptorTransmitterChannel.put(self.__clientSocket)
        #
        #         ColorPrinter.print_important_data("Success to accept client socket", f"{clientSocket}")
        #
        #     except KeyboardInterrupt:
        #         print('server stopped')
        #         self.killAllTask()
        #
        #     except socket.error:
        #         sleep(0.5)
        #
        #     except Exception as e:
        #         self.killAllTask()

