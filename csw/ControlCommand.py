from dataclasses import dataclass
from typing import List
from csw.Parameter import Parameter


@dataclass
class ControlCommand:
    """
    Represents a CSW command.
    """
    source: str
    commandName: str
    maybeObsId: List[str]
    paramSet: List[Parameter]

    @staticmethod
    def fromDict(obj):
        """
        Returns a ControlCommand for the given dict.
        """
        typ = obj["_type"]
        source = obj['source']
        commandName = obj['commandName']
        maybeObsId = obj['maybeObsId'] if 'maybeObsId' in obj else ""
        paramSet = list(map(lambda p: Parameter.fromDict(p), obj['paramSet']))
        assert (typ in {"Setup", "Observe"})
        if typ == 'Setup':
            return Setup(source, commandName, maybeObsId, paramSet)
        else:
            return Observe(source, commandName, maybeObsId, paramSet)

    def asDict(self):
        """
        :return: a dictionary corresponding to this object
        """
        d = {
            '_type': self.__class__.__name__,
            'source': self.source,
            'commandName': self.commandName,
            'paramSet': list(map(lambda p: p.asDict(), self.paramSet))
        }
        if len(self.maybeObsId) != 0:
            d['maybeObsId'] = self.maybeObsId

        return d

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


@dataclass
class Setup(ControlCommand):
    pass


@dataclass
class Observe(ControlCommand):
    pass
