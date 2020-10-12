from dataclasses import dataclass
from typing import List
from csw.Parameter import Parameter


@dataclass
class CurrentState:
    """
    Represents the current state of a python based CSW component.
    """
    prefix: str
    stateName: str
    paramSet: List[Parameter]

    @staticmethod
    def _fromDict(obj):
        """
        Returns a CurrentState for the given dict.
        """
        typ = obj['_type']
        prefix = obj['prefix']
        stateName = obj['stateName']
        paramSet = list(map(lambda p: Parameter._fromDict(p), obj['paramSet']))
        return CurrentState(prefix, stateName, paramSet)

    def _asDict(self):
        """
        Returns: dict
            a dictionary corresponding to this object
        """
        d = {
            'prefix': self.prefix,
            'stateName': self.stateName,
            'paramSet': list(map(lambda p: p._asDict(), self.paramSet))
        }
        return d

    def get(self, keyName: str):
        """
        Gets the parameter with the given name, or else returns None

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
