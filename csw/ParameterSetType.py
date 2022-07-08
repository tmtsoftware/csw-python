from dataclasses import dataclass
from typing import List
from csw.Parameter import Parameter
from csw.Prefix import Prefix


@dataclass
class CommandName:
    """
    A wrapper class representing the name of a Command
    """
    name: str


@dataclass
class SequenceCommand:
    """
    Represents a CSW command.
    """
    source: Prefix
    commandName: CommandName
    maybeObsId: List[str]
    paramSet: List[Parameter]

    # noinspection PyProtectedMember
    @staticmethod
    def _fromDict(obj):
        """
        Returns a ControlCommand for the given dict.
        """
        typ = obj["_type"]
        source = Prefix.from_str(obj['source'])
        commandName = CommandName(obj['commandName'])
        maybeObsId = obj['maybeObsId'] if 'maybeObsId' in obj else ""
        paramSet = list(map(lambda p: Parameter._fromDict(p), obj['paramSet']))
        assert (typ in {"Setup", "Observe", "Wait"})
        match typ:
            case 'Setup':
                return Setup(source, commandName, maybeObsId, paramSet)
            case 'Observe':
                return Observe(source, commandName, maybeObsId, paramSet)
            case 'Wait':
                return Wait(source, commandName, maybeObsId, paramSet)
            case _:
                raise TypeError

    # noinspection PyProtectedMember
    def _asDict(self):
        """
        Returns: dict
            a dictionary corresponding to this object
        """
        d = {
            '_type': self.__class__.__name__,
            'source': str(self.source),
            'commandName': self.commandName.name,
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
class ControlCommand(SequenceCommand):
    pass


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


@dataclass
class Wait(SequenceCommand):
    """
    A Wait command can only be sent to a sequencer
    """
    pass