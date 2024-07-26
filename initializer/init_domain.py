from acceptor.service.socket_accept_service_impl import SocketAcceptServiceImpl
from ipc_queue.repository.ipc_queue_repository_impl import IPCQueueRepositoryImpl
from ipc_queue.service.ipc_queue_service_impl import IPCQueueServiceImpl
from receiver.service.receiver_service_impl import ReceiverServiceImpl
from server_socket.service.server_socket_service_impl import ServerSocketServiceImpl
from task_worker.service.task_worker_service_impl import TaskWorkerServiceImpl
from transmitter.service.transmitter_service_impl import TransmitterServiceImpl


class DomainInitializer:
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

        socketAcceptService = SocketAcceptServiceImpl.getInstance()
        socketAcceptService.requestToInjectAcceptorReceiverChannel(ipcAcceptorReceiverChannel)

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

    @staticmethod
    def initEachDomain():
        DomainInitializer.initIPCQueueDomain()
        DomainInitializer.initTaskWorkerDomain()
        DomainInitializer.initServerSocketDomain()
        DomainInitializer.initSocketAcceptDomain()
        DomainInitializer.initReceiverDomain()
        DomainInitializer.initTransmitterDomain()

