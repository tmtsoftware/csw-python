from dataclasses import dataclass, asdict


@dataclass
class Tag:
    """
    A tag is a label to indicate the use of the coordinate
    """
    name: str


@dataclass
class Angle:
    """
    A wrapper for angle. Normally angle would be stored in double
    as radians, but this introduces rounding errors.
    This class stores value in microarc seconds to prevent rounding errors.
    """
    uas: int


@dataclass
class EqFrame:
    """
    This class is represented as a sealed trait with case objects in Scala and is serialized as: type: {}
    """
    type: str


@dataclass
class ProperMotion:
    pmx: float
    pmy: float


@dataclass
class EqCoord:
    tag: Tag = Tag("BASE")
    ra: Angle = Angle(0)
    dec: Angle = Angle(0)
    frame: EqFrame = "ICRS"
    catalogName: str = "none"
    pm: ProperMotion = ProperMotion(0.0, 0.0)

    def asDict(self):
        return {
            "EqCoord": {
                "tag": asdict(self.tag),
                "ra": asdict(self.ra),
                "dec": asdict(self.dec),
                "frame": {self.frame.type: {}},
                "catalogName": self.catalogName,
                "pm": asdict(self.pm)
            }
        }

    @staticmethod
    def fromDict(obj):
        dict = obj["EqCoord"]
        tag = Tag(**dict["tag"])
        ra = Angle(**dict["ra"])
        dec = Angle(**dict["dec"])
        frame = EqFrame(list(dict["frame"].keys())[0])
        catalogName = dict["catalogName"]
        pm = ProperMotion(**dict["pm"])
        return EqCoord(tag, ra, dec, frame, catalogName, pm)
