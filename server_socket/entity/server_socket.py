import atexit


class ServerSocket(object):
    def __init__(self, host, port, serverSocket):
        self.__host = host
        self.__port = port
        self.__serverSocket = serverSocket

        atexit.register(self.closeSocket)

    def getServerSocket(self):
        return self.__serverSocket

    def getHost(self):
        return self.__host

    def getPort(self):
        return self.__port

    def closeSocket(self):
        self.__serverSocket.close()
