from csw.ObsId import ObsId
from csw.ParameterSetType import Setup, CommandName, Observe, SequenceCommand
from csw.Prefix import Prefix
from esw.Sequence import Sequence


class CommandServiceDsl:

    # todo: can the prefix be defaulted by the prefix of the sequencer? or a prefix dsl property can be provided?
    def Setup(self, sourcePrefix: str, commandName: str, obsId: str | None = None) -> Setup:
        """
        Method to create an instance of Setup

        Args:
            sourcePrefix: Prefix string used to create Prefix representing source of the command
            commandName: representing the name as an identifier of a command
            obsId: an optional parameter represents a unique observation id
        """
        maybeObsId = ObsId.make(obsId) if obsId else None
        return Setup(Prefix.from_str(sourcePrefix), CommandName(commandName), maybeObsId)

    def Observe(self, sourcePrefix: str, commandName: str, obsId: str | None = None) -> Observe:
        """
        Method to create an instance of [[csw.params.commands.Observe]]

        Args:
            sourcePrefix: Prefix string used to create Prefix representing source of the command
            commandName: representing the name as an identifier of a command
            obsId: an optional parameter represents a unique observation id
        """
        maybeObsId = ObsId.make(obsId) if obsId else None
        return Observe(Prefix.from_str(sourcePrefix), CommandName(commandName), maybeObsId)

    def sequenceOf(self, *sequenceCommand: SequenceCommand) -> Sequence:
        """
        Method to create an instance of [[csw.params.commands.Sequence]]

        Args:
            sequenceCommand: list of sequence commands to create sequence
        """
        return Sequence(list(sequenceCommand))
