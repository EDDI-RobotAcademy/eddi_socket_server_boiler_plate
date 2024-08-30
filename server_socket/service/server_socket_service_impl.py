import os
import socket

from server_socket.repository.server_socket_repository_impl import ServerSocketRepositoryImpl
from server_socket.service.server_socket_service import ServerSocketService

from datetime import datetime as dt

from utility.color_print import ColorPrinter


class ServerSocketServiceImpl(ServerSocketService):
    __instance = None

    ONLY_ONE = 1

    def __new__(cls):
        if cls.__instance is None:
            cls.__instance = super().__new__(cls)
            cls.__instance.__serverSocketRepository = ServerSocketRepositoryImpl.getInstance()

        return cls.__instance

    @classmethod
    def getInstance(cls):
        if cls.__instance is None:
            cls.__instance = cls()

        return cls.__instance

    def createServerSocket(self):
        return self.__serverSocketRepository.create()

    def checkServerSocketAlreadyExist(self):
        createdServerSocket = self.__serverSocketRepository.getServerSocket()
        if createdServerSocket:
            try:
                fileDescriptor = createdServerSocket.fileno()
                print(f"Socket is open with fileDescriptor: {fileDescriptor}")
                return True
            except socket.error:
                print("Socket is closed!")
        else:
            print("Socket is not initialized!")
            return False

    def easyToReuseSocket(self):
        self.__serverSocketRepository.reuseSocket()

    def tcpKeepAlive(self):
        self.__serverSocketRepository.keepAlive()

    # def startServerSocket(self, queueList, pid):
    def prepareServerSocket(self):
        ColorPrinter.print_important_data("socket server started", f"{dt.now()}")

        if not self.checkServerSocketAlreadyExist():
            return

        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as serverSocketObject:
            self.easyToReuseSocket()
            # TODO: KEEP_ALIVE
            self.tcpKeepAlive()

            try:
                self.__serverSocketRepository.addressBind()
                self.__serverSocketRepository.howManyListen(self.ONLY_ONE)

                self.pid = os.getpid()
                ColorPrinter.print_important_data("created main socket process", f"{self.pid}")

                self.__serverSocketRepository.setNonBlock()
            except Exception as e:
                # self.killAllTask()
                ColorPrinter.print_important_data("prepareServerSocket() Exception", str(e))

    