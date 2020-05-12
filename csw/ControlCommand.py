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
    def _fromDict(obj):
        """
        Returns a ControlCommand for the given dict.
        """
        typ = obj["_type"]
        source = obj['source']
        commandName = obj['commandName']
        maybeObsId = obj['maybeObsId'] if 'maybeObsId' in obj else ""
        paramSet = list(map(lambda p: Parameter._fromDict(p), obj['paramSet']))
        assert (typ in {"Setup", "Observe"})
        if typ == 'Setup':
            return Setup(source, commandName, maybeObsId, paramSet)
        else:
            return Observe(source, commandName, maybeObsId, paramSet)

    def _asDict(self):
        """
        Returns: dict
            a dictionary corresponding to this object
        """
        d = {
            '_type': self.__class__.__name__,
            'source': self.source,
            'commandName': self.commandName,
            'paramSet': list(map(lambda p: p._asDict(), self.paramSet))
        }
        if len(self.maybeObsId) != 0:
            d['maybeObsId'] = self.maybeObsId

        return d

    def get(self, keyName: str):
        """
        Gets the parameter with the given name, or else returns None.

        Args:
            keyName (str): parameter name

        Returns: Parameter|None
            the parameter, if found
        """
        for p in self.paramSet:
            if p.keyName == keyName:
                return p

    def exists(self, keyName: str):
        """
        Returns true if the parameter with the given name is present

        Args:
            keyName (str): parameter name

        Returns: bool
            true if the parameter is found
        """
        for p in self.paramSet:
            if p.keyName == keyName:
                return True
        return False


@dataclass
class Setup(ControlCommand):
    """
    A Setup is a command that can be sent to an HCD or Assembly.
    """
    pass


@dataclass
class Observe(ControlCommand):
    """
    An Observe is a special command that can be sent to an HCD or Assembly.
    """
    pass
