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
    def fromDict(obj):
        """
        Returns a CurrentState for the given dict.
        """
        # XXX TODO FIXME: Test this: Does it use "_type"?
        # typ = next(iter(obj))
        typ = obj['_type']
        # obj = obj[typ]
        prefix = obj['prefix']
        stateName = obj['stateName']
        paramSet = list(map(lambda p: Parameter.fromDict(p), obj['paramSet']))
        return CurrentState(prefix, stateName, paramSet)

    def asDict(self):
        """
        :return: a dictionary corresponding to this object
        """
        d = {
            'prefix': self.prefix,
            'stateName': self.stateName,
            'paramSet': list(map(lambda p: p.asDict(), self.paramSet))
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
