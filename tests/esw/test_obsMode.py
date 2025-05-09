from csw.Subsystem import Subsystem
from csw.Prefix import Prefix
from esw.ObsMode import ObsMode


def test_obsmode():
    """
    create obsMode from given prefix | ESW-561
    """
    prefix1 = Prefix(Subsystem.IRIS, "IRIS_ImagerAndIFS.variation1")
    prefix2 = Prefix(Subsystem.IRIS, "IRIS_ImagerAndIFS")
    assert ObsMode.fromPrefix(prefix1) == ObsMode("IRIS_ImagerAndIFS")
    assert ObsMode.fromPrefix(prefix2) == ObsMode("IRIS_ImagerAndIFS")
