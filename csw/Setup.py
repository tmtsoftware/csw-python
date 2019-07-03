from dataclasses import dataclass
from typing import List
from csw.Parameter import Parameter

# {
#     "Setup": {
#         "runId": "e0dab300-3290-4c4d-8050-addf2605bdad",
#         "source": "a.b",
#         "commandName": "blah",
#         "maybeObsId": [
#             "dfsd"
#         ],
#         "paramSet": [
#
#         ]
#     }
# }


@dataclass
class Setup:
    """
    Represents a CSW command.
    """
    runId: str
    source: str
    commandName: str
    maybeObsId: List[str]
    paramSet: List[Parameter]

    @staticmethod
    def fromDict(data):
        """
        Returns a Event for the given CBOR object.
        """
        # key = next(iter(data))
        # print("XXX key = " + key)
        # assert(key == "Setup")
        # obj = data[key]
        obj = data
        runId = obj['runId']
        source = obj['source']
        commandName = obj['commandName']
        maybeObsId = obj['maybeObsId']
        paramSet = list(map(lambda p: Parameter.fromDict(p), obj['paramSet']))
        return Setup(runId, source, commandName, maybeObsId, paramSet)

    def asDict(self):
        """
        :return: dictionary to be encoded to CBOR
        """
        return {"Setup": {
            'runId': self.runId,
            'source': self.source,
            'commandName': self.commandName,
            'maybeObsId': self.maybeObsId,
            'paramSet': list(map(lambda p: p.asDict(), self.paramSet))
        }}

    def get(self, keyName: str):
        """
        Gets the parameter with the given name, or else returns None
        :param str keyName: parameter name
        :return: the parameter, if found
        """
        for p in self.paramSet:
            if p.keyName == keyName:
                return p

    def exists(self, keyName: str):
        """
        Returns true if the parameter with the given name is present
        :param str keyName: parameter name
        :return: true if the parameter is found
        """
        for p in self.paramSet:
            if p.keyName == keyName:
                return True
        return False
