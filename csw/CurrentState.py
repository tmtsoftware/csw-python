import traceback
from dataclasses import dataclass
from typing import List, TypeVar
from csw.Parameter import Parameter, Key, KeyType
from csw.Prefix import Prefix

T = TypeVar('T')


# noinspection PyPep8Naming
@dataclass
class CurrentState:
    """
    Represents the current state of a python based CSW component.
    """
    prefix: Prefix
    stateName: str
    paramSet: List[Parameter]

    @staticmethod
    def _fromDict(obj):
        """
        Returns a CurrentState for the given dict.
        """
        prefix = Prefix.from_str(obj['prefix'])
        stateName = obj['stateName']
        paramSet = list(map(lambda p: Parameter._fromDict(p), obj['paramSet']))
        return CurrentState(prefix, stateName, paramSet)

    def _asDict(self):
        """
        Returns: dict
            a dictionary corresponding to this object
        """
        return {
            'prefix': str(self.prefix),
            'stateName': self.stateName,
            'paramSet': list(map(lambda p: p._asDict(), self.paramSet))
        }

    def __call__(self, key: Key[T]) -> Parameter[T] | None:
        """
        This is similar to Scala's apply() method and gets the parameter for the given key, or else returns None.

        Args:
            key (Key[T]): parameter key

        Returns: Parameter[T] | None
            the parameter, if found
        """
        for p in self.paramSet:
            if p.keyName == key.keyName:
                return p

    # noinspection PyUnusedLocal
    def get(self, keyName: str, keyType: KeyType[T]) -> Parameter[T] | None:
        """
        Gets the parameter with the given name, or else returns None.

        Args:
            keyName (str): parameter name
            keyType (KeyType[T]): parameter key type (used only for type hint: See also gets(keyName))

        Returns: Parameter[T] | None
            the parameter, if found
        """
        for p in self.paramSet:
            if p.keyName == keyName:
                return p

    def gets(self, keyName: str) -> Parameter | None:
        """
        Gets the parameter with the given name, or else returns None.

        Args:
            keyName (str): parameter name

        Returns: Parameter | None
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
