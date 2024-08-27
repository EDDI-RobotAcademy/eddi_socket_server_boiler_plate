from utility.color_print import ColorPrinter


class ChannelSelector:

    @staticmethod
    def findUserDefinedReceiverChannel(decodedData):
        protocolNumber = decodedData[0]

        ColorPrinter.print_important_data("protocolNumber", protocolNumber)
        if protocolNumber in (1, 2):
            return True

        return False