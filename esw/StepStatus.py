from dataclasses import dataclass


@dataclass
class StepStatus:
    def _asDict(self) -> dict:
        """
        Returns: a dictionary corresponding to this object
        """
        return {
            "_type": self.__class__.__name__,
        }

    # noinspection PyProtectedMember
    @staticmethod
    def _fromDict(obj):
        """
        Returns a ControlCommand for the given dict.
        """
        typ = obj["_type"]
        match typ:
            case 'Pending':
                return Pending
            case 'InFlight':
                return InFlight
            case 'Success':
                return Success
            case 'Failure':
                return Failure._fromDict(obj)
            case _:
                raise TypeError


@dataclass
class Pending(StepStatus):
    pass


@dataclass
class InFlight(StepStatus):
    pass


@dataclass
class Success(StepStatus):
    pass


@dataclass
class Failure(StepStatus):
    message: str

    def _asDict(self):
        """
        Returns: a dictionary corresponding to this object
        """
        return {
            "_type": self.__class__.__name__,
            "message": self.message
        }

    @staticmethod
    def _fromDict(obj):
        """
        Returns a ControlCommand for the given dict.
        """
        message = obj["message"]
        return Failure(message)
