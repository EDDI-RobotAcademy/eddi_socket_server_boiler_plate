class PacketLengthRequest:
    def __init__(self, packetDataLength):
        self.protocolNumber = 7777
        self.packetDataLength = packetDataLength

    def getPacketDataLength(self):
        return self.packetDataLength

    def toFixedSizeDictionary(self):
        protocolNumberString = str(self.protocolNumber).ljust(4)
        packetDataLengthString = str(self.packetDataLength).ljust(8)

        return {
            "protocolNumber": protocolNumberString,
            "packetDataLength": packetDataLengthString
        }

    def __str__(self):
        return f"PacketLengthRequest(protocolNumber={self.protocolNumber}, packetDataLength={self.packetDataLength})"
