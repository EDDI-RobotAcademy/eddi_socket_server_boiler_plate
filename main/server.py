import colorama
from colorama import Fore, Style

from acceptor.service.socket_accept_service_impl import SocketAcceptServiceImpl
from initializer.init_domain import DomainInitializer
from server_socket.service.server_socket_service_impl import ServerSocketServiceImpl
from task_worker.service.task_worker_service_impl import TaskWorkerServiceImpl
from utility.color_print import ColorPrinter

DomainInitializer.initEachDomain()


if __name__ == '__main__':
    colorama.init(autoreset=True)

    serverSocketService = ServerSocketServiceImpl.getInstance()
    serverSocket = serverSocketService.createServerSocket()
    serverSocketService.prepareServerSocket()
    ColorPrinter.print_important_message("Success to create Server Socket")

    socketAcceptService = SocketAcceptServiceImpl.getInstance()
    socketAcceptService.requestToInjectServerSocket(serverSocket)
    ColorPrinter.print_important_message("Success to inject server socket to acceptor")

    receiverService = ReceiverServiceImpl.getInstance()
    receiverService.requestToInjectClientSocket()

    taskWorkerService = TaskWorkerServiceImpl.getInstance()
    taskWorkerService.createTaskWorker("Acceptor", socketAcceptService.requestToAcceptClient)
    taskWorkerService.executeTaskWorker("Acceptor")

    # transmitterController = TransmitterControllerImpl.getInstance()
    # transmitterController.requestToInjectSocketClient(clientSocket)


    # taskWorkerService.createTaskWorker("Transmitter", )
    # server = SocketServer('0.0.0.0', )
    # server.start()