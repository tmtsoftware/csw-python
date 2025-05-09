from enum import Enum


class UpperCaseEnum(Enum):
    @classmethod
    def fromString(cls, s: str):
        match s:
            case "Container":
                u = s
            case _:
                u = s.upper()
        if u in cls._member_names_:
            return cls[u]
        raise KeyError(f"{u} is not a member of Enum ({', '.join(cls._member_names_)})")

    @classmethod
    def list(cls):
        return list(map(lambda c: c.value, cls))
