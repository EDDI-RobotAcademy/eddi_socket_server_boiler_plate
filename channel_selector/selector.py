import json

from utility.color_print import ColorPrinter


class ChannelSelector:

    @staticmethod
    def findUserDefinedReceiverChannel(decodedData):
        data = json.loads(decodedData)
        protocolNumber = data.get("protocolNumber")

        ColorPrinter.print_important_data("protocolNumber", protocolNumber)
        if protocolNumber in (1, 2):
            return False

        return True