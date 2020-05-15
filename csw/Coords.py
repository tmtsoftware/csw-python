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
    """
    Enum type: Represents the possible values for a Solar System Object.
    """
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
class Coord:
    """
    This is the base class of the coordinate types.
    If the key type is CoordKey, the value type can be any of the Coord subtypes.
    The dict key gives the class name.

    Args:
        tag (Tag): a label to indicate the use of the coordinate

    """
    tag: Tag

    @staticmethod
    def _fromDict(obj: dict):
        switcher = {
            "EqCoord": EqCoord,
            "SolarSystemCoord": SolarSystemCoord,
            "MinorPlanetCoord": MinorPlanetCoord,
            "CometCoord": CometCoord,
            "AltAzCoord": AltAzCoord
        }
        typ = obj["_type"]
        return switcher[typ]._fromValueDict(obj)

    def _asDict(self):
        pass


# noinspection PyUnresolvedReferences
@dataclass
class EqCoord(Coord):
    """
    Represents equatorial coordinates (mirrors class of same name in the CSW Scala code).
    """
    ra: Angle
    dec: Angle
    frame: EqFrame
    catalogName: str
    pm: ProperMotion

    @staticmethod
    def make(tag: str = "BASE", ra: any = "0 deg", dec: any = "0 deg", frame: EqFrame = EqFrame.ICRS,
             catalogName: str = "none", pm: tuple = (0.0, 0.0)):
        """
        Convenience factory method.
        Note that the ra and dec args should be in a format accepted by astropy's Angle class.
        """
        return EqCoord(Tag(tag), Angle(ra), Angle(dec), frame, catalogName, ProperMotion(pm[0], pm[1]))

    def _asDict(self):
        return {
            "_type": self.__class__.__name__,
            "tag": self.tag.name,
            "ra": _CswAngle.fromAngle(self.ra).uas,
            "dec": _CswAngle.fromAngle(self.dec).uas,
            "frame": self.frame.name,
            "catalogName": self.catalogName,
            "pm": asdict(self.pm)
        }

    @staticmethod
    def _fromValueDict(obj: dict):
        return EqCoord(
            tag=Tag(obj["tag"]),
            ra=_CswAngle(obj["ra"]).toAngle().to(u.deg),
            dec=_CswAngle(obj["dec"]).toAngle().to(u.deg),
            frame=EqFrame[obj["frame"]],
            catalogName=obj["catalogName"],
            pm=ProperMotion(**obj["pm"]),
        )


@dataclass
class SolarSystemCoord(Coord):
    """
    Represents Solar System Coordinates (mirrors class of same name in the CSW Scala code).
    """
    body: SolarSystemObject

    @staticmethod
    def make(tag: str, body: SolarSystemObject):
        return SolarSystemCoord(Tag(tag), body)

    def _asDict(self):
        return {
            "_type": self.__class__.__name__,
            "tag": self.tag.name,
            "body": self.body.name,
        }

    @staticmethod
    def _fromValueDict(obj: dict):
        return SolarSystemCoord(
            tag=Tag(obj["tag"]),
            body=SolarSystemObject[obj["body"]]
        )


# noinspection PyUnresolvedReferences
@dataclass
class MinorPlanetCoord(Coord):
    """
    Represents Minor Planet Coordinates (mirrors class of same name in the CSW Scala code).
    """
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

    def _asDict(self):
        return {
            "_type": self.__class__.__name__,
            "tag": self.tag.name,
            "epoch": self.epoch,
            "inclination": _CswAngle.fromAngle(self.inclination).uas,
            "longAscendingNode": _CswAngle.fromAngle(self.longAscendingNode).uas,
            "argOfPerihelion": _CswAngle.fromAngle(self.argOfPerihelion).uas,
            "meanDistance": self.meanDistance,
            "eccentricity": self.eccentricity,
            "meanAnomaly": _CswAngle.fromAngle(self.meanAnomaly).uas
        }

    @staticmethod
    def _fromValueDict(obj: dict):
        return MinorPlanetCoord(
            tag=Tag(obj["tag"]),
            epoch=obj["epoch"],
            inclination=_CswAngle(obj["inclination"]).toAngle().to(u.deg),
            longAscendingNode=_CswAngle(obj["longAscendingNode"]).toAngle().to(u.deg),
            argOfPerihelion=_CswAngle(obj["argOfPerihelion"]).toAngle().to(u.deg),
            meanDistance=obj["meanDistance"],
            eccentricity=obj["eccentricity"],
            meanAnomaly=_CswAngle(obj["meanAnomaly"]).toAngle().to(u.deg)
        )


# noinspection PyUnresolvedReferences
@dataclass
class CometCoord(Coord):
    """
    Represents Comet Coordinates (mirrors class of same name in the CSW Scala code).
    """
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
        return CometCoord(Tag(tag), epochOfPerihelion, Angle(inclination), Angle(longAscendingNode),
                          Angle(argOfPerihelion),
                          perihelionDistance, eccentricity)

    def _asDict(self):
        return {
            "_type": self.__class__.__name__,
            "tag": self.tag.name,
            "epochOfPerihelion": self.epochOfPerihelion,
            "inclination": _CswAngle.fromAngle(self.inclination).uas,
            "longAscendingNode": _CswAngle.fromAngle(self.longAscendingNode).uas,
            "argOfPerihelion": _CswAngle.fromAngle(self.argOfPerihelion).uas,
            "perihelionDistance": self.perihelionDistance,
            "eccentricity": self.eccentricity
        }

    @staticmethod
    def _fromValueDict(obj: dict):
        return CometCoord(
            tag=Tag(obj["tag"]),
            epochOfPerihelion=obj["epochOfPerihelion"],
            inclination=_CswAngle(obj["inclination"]).toAngle().to(u.deg),
            longAscendingNode=_CswAngle(obj["longAscendingNode"]).toAngle().to(u.deg),
            argOfPerihelion=_CswAngle(obj["argOfPerihelion"]).toAngle().to(u.deg),
            perihelionDistance=obj["perihelionDistance"],
            eccentricity=obj["eccentricity"]
        )


# noinspection PyUnresolvedReferences
@dataclass
class AltAzCoord(Coord):
    """
    Represents Alt-Az Coordinates (mirrors class of same name in the CSW Scala code).
    """
    alt: Angle = Angle("0 deg")
    az: Angle = Angle("0 deg")

    @staticmethod
    def make(tag: str = "BASE", alt: any = "0 deg", az: any = "0 deg"):
        """
        Convenience factory method.
        Note that the alt and az args should be in a format accepted by astropy's Angle class.
        """
        return AltAzCoord(Tag(tag), Angle(alt), Angle(az))

    def _asDict(self):
        return {
            "_type": self.__class__.__name__,
            "tag": self.tag.name,
            "alt": _CswAngle.fromAngle(self.alt).uas,
            "az": _CswAngle.fromAngle(self.az).uas
        }

    @staticmethod
    def _fromValueDict(obj: dict):
        return AltAzCoord(
            tag=Tag(obj["tag"]),
            alt=_CswAngle(obj["alt"]).toAngle().to(u.deg),
            az=_CswAngle(obj["az"]).toAngle().to(u.deg),
        )
