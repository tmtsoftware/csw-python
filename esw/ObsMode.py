from dataclasses import dataclass

from csw.Prefix import Prefix


@dataclass
class ObsMode:
    """
    Model which represents the observation mode of the sequencer
    """
    name: str

    @classmethod
    def fromPrefix(cls, sequencerPrefix: Prefix):
        """
        Retrieves ObsMode from given Sequencer Prefix.

        Args:
            sequencerPrefix – Examples IRIS.IRIS_IFS.ONE -> ObsMode(IRIS_IFS), IRIS.IRIS_IMAGER -> ObsMode(IRIS_IMAGER)
        Returns:
            ObsMode
        """
        parts = sequencerPrefix.componentName.split('.', 1)
        return cls(parts[0])
