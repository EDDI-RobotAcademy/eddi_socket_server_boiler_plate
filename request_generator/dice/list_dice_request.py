from request_generator.base_request import BaseRequest
from request_generator.request_type import RequestType


class ListDiceRequest(BaseRequest):
    def __init__(self):
        self.protocolNumber = RequestType.LIST_DICE.value

    def toDictionary(self):
        return {"protocolNumber": self.protocolNumber}

    def __str__(self):
        return f"ListDiceRequest(protocolNumber={self.protocolNumber})"