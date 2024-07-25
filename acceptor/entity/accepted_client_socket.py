import atexit

class AcceptedClientSocket:
    def __init__(self, clientSocket, clientAddress):
        self.__clientSocket = clientSocket
        self.__clientAddress = clientAddress

        atexit.register(self.closeSocket)

    def getClientSocket(self):
        return self.__clientSocket

    def getClientAddress(self):
        return self.__clientAddress

    def closeSocket(self):
        self.__clientSocket.close()

