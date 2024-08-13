from decouple import config

from acceptor.service.socket_accept_service_impl import SocketAcceptServiceImpl
from default_protocol.entity.default_protocol import DefaultProtocolNumber
from default_protocol.service.custom_protocol_service_impl import CustomProtocolServiceImpl
from ipc_queue.repository.ipc_queue_repository_impl import IPCQueueRepositoryImpl
from ipc_queue.service.ipc_queue_service_impl import IPCQueueServiceImpl
from receiver.service.receiver_service_impl import ReceiverServiceImpl
from server_socket.service.server_socket_service_impl import ServerSocketServiceImpl
from ssl_tls.ssl_tls_context_manager import SslTlsContextManager
from task_worker.service.task_worker_service_impl import TaskWorkerServiceImpl
from thread_worker.service.thread_worker_service_impl import ThreadWorkerServiceImpl
from transmitter.service.transmitter_service_impl import TransmitterServiceImpl
from utility.color_print import ColorPrinter


class DomainInitializer:

    # @staticmethod
    # def initCustomProtocolDomain():
    #     customProtocolService = CustomProtocolServiceImpl.getInstance()
    #     diceService = DiceServiceImpl.getInstance()
    #
    #     # 디폴트 프로토콜 등록을 여기서 했음
    #     customProtocolService.registerCustomProtocol(
    #         DefaultProtocolNumber.ROLL_DICE,
    #         diceService.rollDice
    #     )
    #
    #     customProtocolService.registerCustomProtocol(
    #         DefaultProtocolNumber.LIST_DICE,
    #         diceService.diceList
    #     )

    @staticmethod
    def initThreadWorkerDomain():
        ThreadWorkerServiceImpl.getInstance()

    @staticmethod
    def initIPCQueueDomain():
        ipcQueueService = IPCQueueServiceImpl.getInstance()
        ipcQueueService.createDefaultIPCQueue()

    @staticmethod
    def initTaskWorkerDomain():
        TaskWorkerServiceImpl.getInstance()

    @staticmethod
    def initServerSocketDomain():
        ServerSocketServiceImpl.getInstance()

    @staticmethod
    def initSocketAcceptDomain():
        socketAcceptService = SocketAcceptServiceImpl.getInstance()

    @staticmethod
    def initReceiverDomain():
        receiverService = ReceiverServiceImpl.getInstance()

    @staticmethod
    def initTransmitterDomain():
        transmitterService = TransmitterServiceImpl.getInstance()

    @staticmethod
    def initEachDomain():
        # DomainInitializer.initCustomProtocolDomain()

        DomainInitializer.initThreadWorkerDomain()

        DomainInitializer.initIPCQueueDomain()
        DomainInitializer.initTaskWorkerDomain()
        DomainInitializer.initServerSocketDomain()
        DomainInitializer.initSocketAcceptDomain()
        DomainInitializer.initReceiverDomain()
        DomainInitializer.initTransmitterDomain()

