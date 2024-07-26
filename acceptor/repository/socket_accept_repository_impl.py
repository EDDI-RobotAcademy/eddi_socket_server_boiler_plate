import multiprocessing
import socket
from time import sleep

from acceptor.entity.accepted_client_socket import AcceptedClientSocket
from acceptor.repository.socket_accept_repository import SocketAcceptRepository
from utility.color_print import ColorPrinter


class SocketAcceptRepositoryImpl(SocketAcceptRepository):
    __instance = None

    __serverSocket = None
    __clientSocket = None

    __ipcAcceptorChannel = None

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
        ColorPrinter.print_important_data("accept repository -> getClientSocket()", f"{self.__clientSocket}")
        return self.__clientSocket

    def killAllTask(self):
        for activeTask in multiprocessing.active_children():
            ColorPrinter.print_important_data("Terminated Task", f"{activeTask.pid}")
            activeTask.terminate()
            activeTask.join()

    def injectSocketServer(self, serverSocket):
        self.__serverSocket = serverSocket

    def injectAcceptChannel(self, ipcAcceptorChannel):
        self.__ipcAcceptorChannel = ipcAcceptorChannel

    def acceptClient(self):
        serverSocketObject = self.__serverSocket.getServerSocket()

        while True:
            try:
                clientSocket, clientAddress = serverSocketObject.accept()
                clientSocket.setblocking(False)

                self.__clientSocket = AcceptedClientSocket(clientSocket, clientAddress)
                self.__ipcAcceptorChannel.put(self.__clientSocket)

                ColorPrinter.print_important_data("Success to accept client socket", f"{clientSocket}")

            except KeyboardInterrupt:
                print('server stopped')
                self.killAllTask()

            except socket.error:
                sleep(0.5)

            except Exception as e:
                self.killAllTask()

