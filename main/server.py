import colorama
from colorama import Fore, Style

from acceptor.service.socket_accept_service_impl import SocketAcceptServiceImpl
from initializer.init_domain import DomainInitializer
from os_detector.detect import OperatingSystemDetector
from os_detector.operating_system import OperatingSystem
from receiver.service.receiver_service_impl import ReceiverServiceImpl
from server_socket.service.server_socket_service_impl import ServerSocketServiceImpl
from ssl_tls.ssl_tls_context_manager import SslTlsContextManager
from task_worker.service.task_worker_service_impl import TaskWorkerServiceImpl
from thread_worker.service.thread_worker_service_impl import ThreadWorkerServiceImpl
from transmitter.service.transmitter_service_impl import TransmitterServiceImpl
from utility.color_print import ColorPrinter

DomainInitializer.initEachDomain()


if __name__ == '__main__':
    colorama.init(autoreset=True)

    detectedOperatingSystem = OperatingSystemDetector.checkCurrentOperatingSystem()
    ColorPrinter.print_important_data("detectedOperatingSystem", detectedOperatingSystem)

    if detectedOperatingSystem is OperatingSystem.UNKNOWN:
        ColorPrinter.print_important_message("범용 운영체제 외에는 실행 할 수 없습니다!")
        exit(1)

    serverSocketService = ServerSocketServiceImpl.getInstance()
    serverSocket = serverSocketService.createServerSocket()
    serverSocketService.prepareServerSocket()
    ColorPrinter.print_important_message("Success to create Server Socket")

    socketAcceptService = SocketAcceptServiceImpl.getInstance()
    socketAcceptService.requestToInjectServerSocket(serverSocket)
    ColorPrinter.print_important_message("Success to inject server socket to acceptor")

    theadWorkerService = ThreadWorkerServiceImpl.getInstance()
    theadWorkerService.createThreadWorker("Acceptor", socketAcceptService.requestToAcceptClient)
    theadWorkerService.executeThreadWorker("Acceptor")

    receiverService = ReceiverServiceImpl.getInstance()

    theadWorkerService.createThreadWorker("Receiver", receiverService.requestToReceiveClient)
    theadWorkerService.executeThreadWorker("Receiver")

    transmitterService = TransmitterServiceImpl.getInstance()

    theadWorkerService.createThreadWorker("Transmitter", transmitterService.requestToTransmitClient)
    theadWorkerService.executeThreadWorker("Transmitter")
