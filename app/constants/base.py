from enum import Enum, IntEnum


class BaseEnum(Enum):
    label: str

    def __new__(cls, value: object, label: str = "") -> "BaseEnum":
        obj = cls.__new__(cls, value)
        obj._value_ = value
        obj.label = label
        return obj

    @classmethod
    def names(cls) -> list[str]:
        return [m.name for m in cls]

    @classmethod
    def values(cls) -> list:
        return [m.value for m in cls]

    @classmethod
    def labels(cls) -> list[str]:
        return [m.label for m in cls]

    @classmethod
    def choices(cls) -> list[dict]:
        return [{"value": m.value, "label": m.label} for m in cls]

    @classmethod
    def description(cls) -> str:
        return ", ".join([f"{m.value}:{m.label}" for m in cls])


class BaseIntEnum(IntEnum):
    label: str

    def __new__(cls, value: int, label: str = "") -> "BaseIntEnum":
        obj = int.__new__(cls, value)
        obj._value_ = value
        obj.label = label
        return obj

    @classmethod
    def names(cls) -> list[str]:
        return [m.name for m in cls]

    @classmethod
    def values(cls) -> list:
        return [m.value for m in cls]

    @classmethod
    def labels(cls) -> list[str]:
        return [m.label for m in cls]

    @classmethod
    def choices(cls) -> list[dict]:
        return [{"value": m.value, "label": m.label} for m in cls]

    @classmethod
    def description(cls) -> str:
        return ", ".join([f"{m.value}:{m.label}" for m in cls])
