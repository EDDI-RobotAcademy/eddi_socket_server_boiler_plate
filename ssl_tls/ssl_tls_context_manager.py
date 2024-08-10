import ssl


class SslTlsContextManager:
    __sslContext = None

    @staticmethod
    def setupSSLContext(certfile, keyfile, cafile):
        if SslTlsContextManager.__sslContext is None:
            SslTlsContextManager.__sslContext = ssl.SSLContext(ssl.PROTOCOL_TLS_SERVER)
            SslTlsContextManager.__sslContext.load_cert_chain(certfile=certfile, keyfile=keyfile)

            SslTlsContextManager.__sslContext.verify_mode = ssl.CERT_REQUIRED
            SslTlsContextManager.__sslContext.load_verify_locations(cafile=cafile)
        else:
            raise RuntimeError("SSL/TLS context is already set up.")

    @staticmethod
    def getSSLContext():
        if SslTlsContextManager.__sslContext is None:
            raise RuntimeError("SSL/TLS context has not been set up yet.")
        return SslTlsContextManager.__sslContext

    @staticmethod
    def initSslTlsContext():
        from decouple import config  # 환경 변수 로드
        # 환경 변수에서 인증서와 키 파일 경로 로드
        serverCertificate = config('SERVER_CERTIFICATE')
        serverKey = config('SERVER_PRIVATE')
        clientCA = config('CLIENT_CA_CERTIFICATE')

        if not serverCertificate or not serverKey or not clientCA:
            raise ValueError("SSL/TLS 설정에 필요한 환경 변수가 누락되었습니다.")

        SslTlsContextManager.setupSSLContext(certfile=serverCertificate, keyfile=serverKey, cafile=clientCA)
        print("SSL/TLS context initialized successfully.")
