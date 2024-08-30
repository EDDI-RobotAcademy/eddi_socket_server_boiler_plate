import socket

import server_socket

from decouple import config

from server_socket.entity.server_socket import ServerSocket
from server_socket.repository.server_socket_repository import ServerSocketRepository
from utility.color_print import ColorPrinter


class ServerSocketRepositoryImpl(ServerSocketRepository):
    __instance = None
    __serverSocket = None

    def __new__(cls):
        if cls.__instance is None:
            cls.__instance = super().__new__(cls)

        return cls.__instance

    @classmethod
    def getInstance(cls):
        if cls.__instance is None:
            cls.__instance = cls()

        return cls.__instance

    def create(self):
        socketObject = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.__serverSocket = ServerSocket(config('HOST'), int(config('PORT')), socketObject)
        ColorPrinter.print_important_data("created socket port", f"{int(config('PORT'))}")
        return self.__serverSocket

    def getServerSocket(self):
        socketObject = self.__serverSocket.getServerSocket()
        return socketObject

    def reuseSocket(self):
        socketObject = self.__serverSocket.getServerSocket()
        socketObject.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

    def keepAlive(self):
        socketObject = self.__serverSocket.getServerSocket()
        socketObject.setsockopt(socket.SOL_SOCKET, socket.SO_KEEPALIVE, 1)

    def addressBind(self):
        socketObject = self.__serverSocket.getServerSocket()
        host = self.__serverSocket.getHost()
        port = self.__serverSocket.getPort()
        socketObject.bind((host, port))

    def howManyListen(self, canListenCount):
        socketObject = self.__serverSocket.getServerSocket()
        socketObject.listen(canListenCount)

    def setNonBlock(self):
        socketObject = self.__serverSocket.getServerSocket()
        socketObject.setblocking(False)

