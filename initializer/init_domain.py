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
        ipcQueueRepository = IPCQueueRepositoryImpl.getInstance()
        ipcAcceptorReceiverChannel = ipcQueueRepository.getIPCAcceptorReceiverChannel()
        ipcAcceptorTransmitterChannel = ipcQueueRepository.getIPCAcceptorTransmitterChannel()

        socketAcceptService = SocketAcceptServiceImpl.getInstance()
        socketAcceptService.requestToInjectAcceptorReceiverChannel(ipcAcceptorReceiverChannel)
        socketAcceptService.requestToInjectAcceptorTransmitterChannel(ipcAcceptorTransmitterChannel)

    @staticmethod
    def initReceiverDomain():
        ipcQueueRepository = IPCQueueRepositoryImpl.getInstance()
        ipcAcceptorReceiverChannel = ipcQueueRepository.getIPCAcceptorReceiverChannel()

        receiverService = ReceiverServiceImpl.getInstance()
        receiverService.requestToInjectAcceptorReceiverChannel(ipcAcceptorReceiverChannel)

    @staticmethod
    def initTransmitterDomain():
        ipcQueueRepository = IPCQueueRepositoryImpl.getInstance()
        ipcAcceptorTransmitterChannel = ipcQueueRepository.getIPCAcceptorTransmitterChannel()

        transmitterService = TransmitterServiceImpl.getInstance()
        transmitterService.requestToInjectAcceptorTransmitterChannel(ipcAcceptorTransmitterChannel)

    # @staticmethod
    # def initSslTlsContext():
    #     # 환경 변수에서 인증서와 키 파일 경로 로드
    #     serverCertificate = config('SERVER_CERTIFICATE')
    #     serverKey = config('SERVER_PRIVATE')
    #     clientCA = config('CLIENT_CA_CERTIFICATE')
    #
    #     if not serverCertificate or not serverKey:
    #         raise ValueError("SSL/TLS 설정에 필요한 환경 변수가 누락되었습니다.")
    #         exit(1)
    #
    #     sslContextManager = SslTlsContextManager.getInstance()
    #     sslContextManager.setupSSLContext(certfile=serverCertificate, keyfile=serverKey, cafile=clientCA)
    #     ColorPrinter.print_important_message("SSL/TLS context initialized successfully.")

    @staticmethod
    def initEachDomain():
        # DomainInitializer.initCustomProtocolDomain()
        # DomainInitializer.initSslTlsContext()

        DomainInitializer.initThreadWorkerDomain()

        DomainInitializer.initIPCQueueDomain()
        DomainInitializer.initTaskWorkerDomain()
        DomainInitializer.initServerSocketDomain()
        DomainInitializer.initSocketAcceptDomain()
        DomainInitializer.initReceiverDomain()
        DomainInitializer.initTransmitterDomain()

