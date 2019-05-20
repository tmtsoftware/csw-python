from dataclasses import dataclass, asdict


@dataclass(frozen=True)
class Tag:
    """
    A tag is a label to indicate the use of the coordinate
    """
    name: str

    def serialize(self):
        """
        :return: a dictionary that can be serialized to CBOR
        """
        return asdict(self)

    @staticmethod
    def deserialize(obj):
        """
        Returns a Tag for the given (decoded) CBOR object.
        """
        return Tag(obj['name'])


@dataclass(frozen=True)
class Angle:
    """
    A wrapper for angle. Normally angle would be stored in double
    as radians, but this introduces rounding errors.
    This class stores value in microarc seconds to prevent rounding errors.
    """
    uas: int

    def serialize(self):
        """
        :return: a dictionary that can be serialized to CBOR
        """
        return asdict(self)

    @staticmethod
    def deserialize(obj):
        """
        Returns an Angle for the given (decoded) CBOR object.
        """
        return Angle(obj['uas'])


@dataclass(frozen=True)
class EqCoord:
    """
    Creates a Struct (value when key is "StructKey").
    'paramSet' is a list of Parameters that make up the Struct
    """
    paramSet: List[Parameter]

    def serialize(self):
        """
        :return: a dictionary that can be serialized to CBOR
        """
        return {"paramSet" : list(map(lambda p: p.serialize(), self.paramSet))}

    @staticmethod
    def deserialize(obj):
        """
        Returns a Stuct for the given (decoded) CBOR object.
        """
        return Struct(list(map(lambda p: Parameter.deserialize(p), obj['paramSet'])))



# case class EqCoord(tag: Tag, ra: Angle, dec: Angle, frame: EQ_FRAME, catalogName: String, pm: ProperMotion) extends Coord {

#    with values: BasePosition: [{'EqCoord': {'tag': {'name': 'BASE'}, 'ra': {'uas': 648000000000}, 'dec': {'uas': 115200000000}, 'frame': {'ICRS': {}}, 'catalogName': 'none', 'pm': {'pmx': 0.5, 'pmy': 2.33}}}]
