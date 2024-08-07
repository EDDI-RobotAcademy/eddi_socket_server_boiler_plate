from .dice.list_dice_request import ListDiceRequest
from .dice.roll_dice_request import RollDiceRequest
from .request_type import RequestType


class RequestClassMap:
    requestClassMap = {
        RequestType.ROLL_DICE.name: RollDiceRequest,
        RequestType.LIST_DICE.name: ListDiceRequest,
    }

    @staticmethod
    def getRequestClass(requestTypeName):
        return RequestClassMap.requestClassMap.get(requestTypeName)
