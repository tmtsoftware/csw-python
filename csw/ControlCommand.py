from dataclasses import dataclass
from typing import List
from csw.Parameter import Parameter


@dataclass
class ControlCommand:
    """
    Represents a CSW command.
    """
    runId: str
    source: str
    commandName: str
    maybeObsId: List[str]
    paramSet: List[Parameter]

    @staticmethod
    def fromDict(obj, flat: bool):
        """
        Returns a ControlCommand for the given dict.
        """
        if flat:
            typ = obj['type']
        else:
            typ = next(iter(obj))
            obj = obj[typ]

        runId = obj['runId']
        source = obj['source']
        commandName = obj['commandName']
        maybeObsId = obj['maybeObsId'] if 'maybeObsId' in obj else ""
        paramSet = list(map(lambda p: Parameter.fromDict(p, flat), obj['paramSet']))
        assert(typ in {"Setup", "Observe"})
        if typ == 'Setup':
            return Setup(runId, source, commandName, maybeObsId, paramSet)
        else:
            return Observe(runId, source, commandName, maybeObsId, paramSet)

    def asDict(self, flat: bool):
        """
        :return: a dictionary corresponding to this object
        """
        d = {
            'runId': self.runId,
            'source': self.source,
            'commandName': self.commandName,
            'paramSet': list(map(lambda p: p.asDict(flat), self.paramSet))
        }
        if len(self.maybeObsId) != 0:
            d['maybeObsId'] = self.maybeObsId
        if flat:
            d['type'] = self.__class__.__name__
        else:
            d = {
                self.__class__.__name__: d
            }
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
