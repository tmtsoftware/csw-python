from dataclasses import dataclass

from csw.Subsystem import Subsystems


@dataclass
class Prefix:
    """
    A class representing a component prefix, made up of the subsystem and the component name.
    Note: Component name should not contain leading or trailing spaces or a hyphen (-).
    """
    subsystem: Subsystems
    componentName: str

    def __post_init__(self):
        assert (self.componentName == self.componentName.strip())
        assert ("-" not in self.componentName)

    def __str__(self):
        return f"{self.subsystem.name}.{self.componentName}"

    @classmethod
    def from_str(cls, prefixStr: str):
        [s, c] = prefixStr.split('.', 1)
        return cls(Subsystems[s.upper()], c)
