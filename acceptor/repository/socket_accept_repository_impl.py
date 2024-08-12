import select
import socket
import ssl
import threading
from time import sleep
from acceptor.entity.accepted_client_socket import AcceptedClientSocket
from acceptor.repository.socket_accept_repository import SocketAcceptRepository
from critical_section.manager import CriticalSectionManager
from ssl_tls.ssl_tls_context_manager import SslTlsContextManager
from utility.color_print import ColorPrinter


class SocketAcceptRepositoryImpl(SocketAcceptRepository):
    __instance = None

    def __new__(cls):
        if cls.__instance is None:
            cls.__instance = super().__new__(cls)
        return cls.__instance

    @classmethod
    def getInstance(cls):
        if cls.__instance is None:
            cls.__instance = cls()
        return cls.__instance

    def __init__(self):
        self.__serverSocket = None
        self.__criticalSectionManager = CriticalSectionManager.getInstance()

    def injectSocketServer(self, serverSocket):
        self.__serverSocket = serverSocket

    def acceptClient(self):
        serverSocketObject = self.__serverSocket.getServerSocket()
        SslTlsContextManager.initSslTlsContext()
        sslContext = SslTlsContextManager.getSSLContext()

        while True:
            try:
                # 클라이언트 연결 수락
                clientSocket, clientAddress = serverSocketObject.accept()
                ColorPrinter.print_important_data("Accepted connection", clientAddress)

                clientSocket.setblocking(False)

                # SSL 핸드셰이크를 비동기적으로 처리하기 위해 별도의 쓰레드 생성
                threading.Thread(
                    target=self.__handle_ssl_handshake,
                    args=(clientSocket, clientAddress, sslContext),
                    daemon=True
                ).start()

            except socket.error:
                sleep(0.5)
            except Exception as e:
                ColorPrinter.print_important_data("Acceptor Error", str(e))

    def __handle_ssl_handshake(self, clientSocket, clientAddress, sslContext):
        try:
            # SSL 소켓으로 래핑
            sslClientSocket = sslContext.wrap_socket(clientSocket, server_side=True, do_handshake_on_connect=False)

            while True:
                try:
                    # SSL 핸드셰이크 시도
                    sslClientSocket.do_handshake()
                    ColorPrinter.print_important_data("SSL handshake successful", clientAddress)
                    break
                except ssl.SSLWantReadError:
                    # 소켓이 읽기 가능할 때까지 대기
                    select.select([sslClientSocket], [], [])
                except ssl.SSLWantWriteError:
                    # 소켓이 쓰기 가능할 때까지 대기
                    select.select([], [sslClientSocket], [])
                except ssl.SSLError as ssl_error:
                    ColorPrinter.print_important_data("(인증되지 않은 사용자) Failed to establish SSL connection", str(ssl_error))
                    clientSocket.close()
                    return

            sslClientSocket.setblocking(False)
            acceptedClientSocket = AcceptedClientSocket(sslClientSocket, clientAddress)
            self.__criticalSectionManager.setClientSocket(acceptedClientSocket)
            ColorPrinter.print_important_data("Success to accept client socket", f"{sslClientSocket}")

        except ssl.SSLError as ssl_error:
            ColorPrinter.print_important_data("(인증되지 않은 사용자) Failed to establish SSL connection", str(ssl_error))
            clientSocket.close()
        except socket.error as e:
            ColorPrinter.print_important_data("Socket Error during SSL handshake", str(e))
            clientSocket.close()
        except Exception as e:
            ColorPrinter.print_important_data("Error during SSL handshake", str(e))
            clientSocket.close()
