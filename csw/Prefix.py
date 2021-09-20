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

    def __init__(self, subsystem: Subsystems, componentName: str):
        assert (componentName == componentName.strip())
        assert ("-" not in componentName)
        self.subsystem = subsystem
        self.componentName = componentName

    def __str__(self):
        return f"{self.subsystem.name}.{self.componentName}"

    @classmethod
    def from_str(class_object, prefixStr: str):
        [s, c] = prefixStr.split('.', 1)
        return class_object(Subsystems[s.upper()], c)
