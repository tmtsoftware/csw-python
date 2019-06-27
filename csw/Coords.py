from dataclasses import dataclass, asdict
from enum import Enum
from astropy.coordinates import Angle
from astropy import units as u


@dataclass
class Tag:
    """
    A tag is a label to indicate the use of the coordinate
    """
    name: str


# noinspection PyUnresolvedReferences
@dataclass
class _CswAngle:
    """
    A wrapper for Angle values (See the csw.params.core.models.Angle class).
    Note: The Python API uses astropy Angle. This class is used internally for compatibility.
    Normally Angle would be stored in double as radians, but this introduces rounding errors.
    This class stores value in microarc seconds to prevent rounding errors.
    """
    uas: int

    def toAngle(self):
        return Angle(self.uas * u.uarcsec)

    @staticmethod
    def fromAngle(a: Angle):
        return _CswAngle(int(a.uarcsec))


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


# noinspection PyUnresolvedReferences
@dataclass
class EqCoord:
    """
    Represents equatorial coordinates (mirrors class of same name in the CSW Scala code).
    """
    tag: Tag = Tag("BASE")
    ra: Angle = Angle("0 deg")
    dec: Angle = Angle("0 deg")
    frame: EqFrame = EqFrame.ICRS
    catalogName: str = "none"
    pm: ProperMotion = ProperMotion(0.0, 0.0)

    @staticmethod
    def make(tag: str = "BASE", ra: any = "0 deg", dec: any = "0 deg", frame: EqFrame = EqFrame.ICRS, catalogName: str = "none", pm: tuple = (0.0, 0.0)):
        """
        Convenience factory method.
        Note that the ra and dec args should be in a format accepted by astropy's Angle class.
        """
        return EqCoord(Tag(tag), Angle(ra), Angle(dec), frame, catalogName, ProperMotion(pm[0], pm[1]))

    def asDict(self):
        return {
            "EqCoord": {
                "tag": asdict(self.tag),
                "ra": asdict(_CswAngle.fromAngle(self.ra)),
                "dec": asdict(_CswAngle.fromAngle(self.dec)),
                "frame": {self.frame.name: {}},
                "catalogName": self.catalogName,
                "pm": asdict(self.pm)
            }
        }

    @staticmethod
    def fromDict(obj: dict):
        return EqCoord(
            tag=Tag(**obj["tag"]),
            ra=_CswAngle(**obj["ra"]).toAngle().to(u.deg),
            dec=_CswAngle(**obj["dec"]).toAngle().to(u.deg),
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

    @staticmethod
    def make(tag: str, body: SolarSystemObject):
        return SolarSystemCoord(Tag(tag), body)

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


# noinspection PyUnresolvedReferences
@dataclass
class MinorPlanetCoord:
    """
    Represents Minor Planet Coordinates (mirrors class of same name in the CSW Scala code).
    """
    tag: Tag
    epoch: float  # TT as a Modified Julian Date
    inclination: Angle
    longAscendingNode: Angle
    argOfPerihelion: Angle
    meanDistance: float  # AU
    eccentricity: float
    meanAnomaly: Angle

    @staticmethod
    def make(tag: str, epoch: float, inclination: any, longAscendingNode: any, argOfPerihelion: any,
             meanDistance: float, eccentricity: float, meanAnomaly: any):
        """
        Convenience factory method.
        Note that the inclination, longAscendingNode, argOfPerihelion and meanAnomaly args
        should be in a format accepted by astropy's Angle class.
        """
        return MinorPlanetCoord(Tag(tag), epoch, Angle(inclination), Angle(longAscendingNode), Angle(argOfPerihelion),
                                meanDistance, eccentricity, Angle(meanAnomaly))

    def asDict(self):
        return {
            "MinorPlanetCoord": {
                "tag": asdict(self.tag),
                "epoch": self.epoch,
                "inclination": asdict(_CswAngle.fromAngle(self.inclination)),
                "longAscendingNode": asdict(_CswAngle.fromAngle(self.longAscendingNode)),
                "argOfPerihelion": asdict(_CswAngle.fromAngle(self.argOfPerihelion)),
                "meanDistance": self.meanDistance,
                "eccentricity": self.eccentricity,
                "meanAnomaly": asdict(_CswAngle.fromAngle(self.meanAnomaly))
            }
        }

    @staticmethod
    def fromDict(obj: dict):
        return MinorPlanetCoord(
            tag=Tag(**obj["tag"]),
            epoch=obj["epoch"],
            inclination=_CswAngle(**obj["inclination"]).toAngle().to(u.deg),
            longAscendingNode=_CswAngle(**obj["longAscendingNode"]).toAngle().to(u.deg),
            argOfPerihelion=_CswAngle(**obj["argOfPerihelion"]).toAngle().to(u.deg),
            meanDistance=obj["meanDistance"],
            eccentricity=obj["eccentricity"],
            meanAnomaly=_CswAngle(**obj["meanAnomaly"]).toAngle().to(u.deg)
        )


# noinspection PyUnresolvedReferences
@dataclass
class CometCoord:
    """
    Represents Comet Coordinates (mirrors class of same name in the CSW Scala code).
    """
    tag: Tag
    epochOfPerihelion: float  # TT as a Modified Julian Date
    inclination: Angle
    longAscendingNode: Angle
    argOfPerihelion: Angle
    perihelionDistance: float  # AU
    eccentricity: float

    @staticmethod
    def make(tag: str, epochOfPerihelion: float, inclination: any, longAscendingNode: any, argOfPerihelion: any,
             perihelionDistance: float, eccentricity: float):
        """
        Convenience factory method.
        Note that the inclination, longAscendingNode and argOfPerihelion args
        should be in a format accepted by astropy's Angle class.
        """
        return CometCoord(Tag(tag), epochOfPerihelion, Angle(inclination), Angle(longAscendingNode), Angle(argOfPerihelion),
                          perihelionDistance, eccentricity)


    def asDict(self):
        return {
            "CometCoord": {
                "tag": asdict(self.tag),
                "epochOfPerihelion": self.epochOfPerihelion,
                "inclination": asdict(_CswAngle.fromAngle(self.inclination)),
                "longAscendingNode": asdict(_CswAngle.fromAngle(self.longAscendingNode)),
                "argOfPerihelion": asdict(_CswAngle.fromAngle(self.argOfPerihelion)),
                "perihelionDistance": self.perihelionDistance,
                "eccentricity": self.eccentricity
            }
        }

    @staticmethod
    def fromDict(obj: dict):
        return CometCoord(
            tag=Tag(**obj["tag"]),
            epochOfPerihelion=obj["epochOfPerihelion"],
            inclination=_CswAngle(**obj["inclination"]).toAngle().to(u.deg),
            longAscendingNode=_CswAngle(**obj["longAscendingNode"]).toAngle().to(u.deg),
            argOfPerihelion=_CswAngle(**obj["argOfPerihelion"]).toAngle().to(u.deg),
            perihelionDistance=obj["perihelionDistance"],
            eccentricity=obj["eccentricity"]
        )


# noinspection PyUnresolvedReferences
@dataclass
class AltAzCoord:
    """
    Represents Alt-Az Coordinates (mirrors class of same name in the CSW Scala code).
    """
    tag: Tag = Tag("BASE")
    alt: Angle = Angle("0 deg")
    az: Angle = Angle("0 deg")

    @staticmethod
    def make(tag: str = "BASE", alt: any = "0 deg", az: any = "0 deg"):
        """
        Convenience factory method.
        Note that the alt and az args should be in a format accepted by astropy's Angle class.
        """
        return AltAzCoord(Tag(tag), Angle(alt), Angle(az))

    def asDict(self):
        return {
            "AltAzCoord": {
                "tag": asdict(self.tag),
                "alt": asdict(_CswAngle.fromAngle(self.alt)),
                "az": asdict(_CswAngle.fromAngle(self.az))
            }
        }

    @staticmethod
    def fromDict(obj: dict):
        return AltAzCoord(
            tag=Tag(**obj["tag"]),
            alt=_CswAngle(**obj["alt"]).toAngle().to(u.deg),
            az=_CswAngle(**obj["az"]).toAngle().to(u.deg),
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