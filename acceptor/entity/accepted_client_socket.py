import atexit

from utility.color_print import ColorPrinter


class AcceptedClientSocket:
    def __init__(self, clientSocket, clientAddress):
        self.__clientSocket = clientSocket
        self.__clientAddress = clientAddress

        ColorPrinter.print_important_message("AcceptedClientSocket Constructor!")

        atexit.register(self.closeSocket)

    def getClientSocket(self):
        return self.__clientSocket

    def getClientAddress(self):
        return self.__clientAddress

    def closeSocket(self):
        self.__clientSocket.close()

