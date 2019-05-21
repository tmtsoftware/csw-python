from dataclasses import dataclass, asdict
from enum import Enum
# import numpy as np
# from astropy import units as u
# from astropy.coordinates import XXXAngle as A

@dataclass
class Tag:
    """
    A tag is a label to indicate the use of the coordinate
    """
    name: str


# TODO: Use astropy's Angle class and convert to this one for compatibility?
# Or implement methods and constants available in Scala class
@dataclass
class Angle:
    """
    A wrapper for angle. Normally angle would be stored in double
    as radians, but this introduces rounding errors.
    This class stores value in microarc seconds to prevent rounding errors.
    """
    uas: int

    #operators
    # def __add__(self, a2):
    #     return Angle(self.uas + a2.uas)
    #
    # def __sub__(self, a2):
    #     return Angle(self.uas - a2.uas)
    #
    # def __mul__(self, a2):
    #     return Angle(self.uas * a2.uas)
    #
    # def __div__(self, a2):
    #     return Angle(self.uas / a2.uas)
    #
    # def __pos__(self):
    #     return self
    #
    # def __neg__(self):
    #     return Angle(-self.uas)

    # @staticmethod
    # def fromAstropyAngle(a):
    #     astropy.
    #


class EqFrame(Enum):
    ICRS = 0
    FK5 = 1


class SolarSystemObject(Enum):
    Mercury = 0
    Venus = 1
    Moon = 2
    Mars = 3
    Jupiter = 4
    Saturn = 5
    Neptune = 6
    Uranus = 7
    Pluto = 8


@dataclass
class ProperMotion:
    pmx: float
    pmy: float


@dataclass
class EqCoord:
    """
    Represents equatorial coordinates (mirrors class of same name in the CSW Scala code).
    """
    tag: Tag = Tag("BASE")
    ra: Angle = Angle(0)
    dec: Angle = Angle(0)
    frame: EqFrame = EqFrame.ICRS
    catalogName: str = "none"
    pm: ProperMotion = ProperMotion(0.0, 0.0)

    def asDict(self):
        return {
            "EqCoord": {
                "tag": asdict(self.tag),
                "ra": asdict(self.ra),
                "dec": asdict(self.dec),
                "frame": {self.frame.name: {}},
                "catalogName": self.catalogName,
                "pm": asdict(self.pm)
            }
        }

    @staticmethod
    def fromDict(obj: dict):
        return EqCoord(
            tag=Tag(**obj["tag"]),
            ra=Angle(**obj["ra"]),
            dec=Angle(**obj["dec"]),
            frame=EqFrame[list(obj["frame"].keys())[0]],
            catalogName=obj["catalogName"],
            pm=ProperMotion(**obj["pm"]),
        )


@dataclass
class SolarSystemCoord:
    """
    Represents Solar System Coordinates (mirrors class of same name in the CSW Scala code).
    """
    tag: Tag
    body: SolarSystemObject

    def asDict(self):
        return {
            "SolarSystemCoord": {
                "tag": asdict(self.tag),
                "body": {self.body.name: {}},
            }
        }

    @staticmethod
    def fromDict(obj: dict):
        return SolarSystemCoord(
            tag=Tag(**obj["tag"]),
            body=SolarSystemObject[list(obj["body"].keys())[0]]
        )


@dataclass
class MinorPlanetCoord:
    """
    Represents Minor Planet Coordinates (mirrors class of same name in the CSW Scala code).
    """
    tag: Tag
    epoch: float  # TT as a Modified Julian Date
    inclination: Angle  # degrees
    longAscendingNode: Angle  # degrees
    argOfPerihelion: Angle  # degrees
    meanDistance: float  # AU
    eccentricity: float
    meanAnomaly: Angle  # degrees

    def asDict(self):
        return {
            "MinorPlanetCoord": asdict(self)
        }

    @staticmethod
    def fromDict(obj: dict):
        return MinorPlanetCoord(
            tag=Tag(**obj["tag"]),
            epoch=obj["epoch"],
            inclination=Angle(**obj["inclination"]),
            longAscendingNode=Angle(**obj["longAscendingNode"]),
            argOfPerihelion=Angle(**obj["argOfPerihelion"]),
            meanDistance=obj["meanDistance"],
            eccentricity=obj["eccentricity"],
            meanAnomaly=Angle(**obj["meanAnomaly"])
        )


@dataclass
class CometCoord:
    """
    Represents Comet Coordinates (mirrors class of same name in the CSW Scala code).
    """
    tag: Tag
    epochOfPerihelion: float  # TT as a Modified Julian Date
    inclination: Angle  # degrees
    longAscendingNode: Angle  # degrees
    argOfPerihelion: Angle  # degrees
    perihelionDistance: float  # AU
    eccentricity: float

    def asDict(self):
        return {
            "CometCoord": asdict(self)
        }

    @staticmethod
    def fromDict(obj: dict):
        return CometCoord(
            tag=Tag(**obj["tag"]),
            epochOfPerihelion=obj["epochOfPerihelion"],
            inclination=Angle(**obj["inclination"]),
            longAscendingNode=Angle(**obj["longAscendingNode"]),
            argOfPerihelion=Angle(**obj["argOfPerihelion"]),
            perihelionDistance=obj["perihelionDistance"],
            eccentricity=obj["eccentricity"]
        )


#  case class AltAzCoord(tag: Tag, alt: Angle, az: Angle) extends Coord {
@dataclass
class AltAzCoord:
    """
    Represents Alt-Az Coordinates (mirrors class of same name in the CSW Scala code).
    """
    tag: Tag
    alt: Angle  # degrees
    az: Angle  # degrees

    def asDict(self):
        return {
            "AltAzCoord": asdict(self)
        }

    @staticmethod
    def fromDict(obj: dict):
        return AltAzCoord(
            tag=Tag(**obj["tag"]),
            alt=Angle(**obj["alt"]),
            az=Angle(**obj["az"]),
        )


class Coord:
    """
    In Scala this is the base trait of the coordinate types.
    If the key type is CoordKey, the value type can be any of the Coord subtypes.
    The dict key gives the class name.
    """

    @staticmethod
    def fromDict(obj: dict):
        switcher = {
            "EqCoord": EqCoord,
            "SolarSystemCoord": SolarSystemCoord,
            "MinorPlanetCoord": MinorPlanetCoord,
            "CometCoord": CometCoord,
            "AltAzCoord": AltAzCoord
        }
        name = list(obj.keys())[0]
        return switcher[name].fromDict(obj[name])
