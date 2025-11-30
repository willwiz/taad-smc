# pyright: reportUnknownMemberType=false, reportUnknownVariableType=false
from collections.abc import Mapping
from typing import Literal, TypeIs, cast, get_args, get_origin, get_type_hints

from .trait import SpecimenInfo, TestProtocol

type JSON_VALUE = None | str | int | float | bool | "JSON_ARRAY" | "JSON_DICT"
type JSON_ARRAY = list[JSON_VALUE]
type JSON_DICT = dict[str, JSON_VALUE]


def is_specimen_info(dct: object) -> TypeIs[SpecimenInfo]:
    """Check if a dictionary conforms to the SpecimenInfo TypedDict.

    Parameters
    ----------
    dct : object
        The dictionary to check.

    Returns
    -------
    bool
        True if the dictionary conforms to the SpecimenInfo TypedDict, False otherwise.

    """
    if not isinstance(dct, Mapping):
        return False
    for key, value_type in get_type_hints(SpecimenInfo).items():
        match dct.get(key):
            case None:
                return False
            case value:
                pass
        if get_origin(value_type) is Literal:
            if value not in get_args(value_type):
                return False
        elif not isinstance(value, value_type):
            return False
    return True


_PROTOCOL_REQUIRED = {
    "Sawtooth": ["max_strain", "duration"],
    "Trapazoid": ["max_strain", "loading", "unloading"],
    "Hold": [],
    "Slack": ["max_strain", "duration", "loading"],
}


def _is_special_protocol_type(val: Mapping[object, object], kind: str) -> bool:
    for req in _PROTOCOL_REQUIRED[kind]:
        match val.get(req):
            case None:
                return False
            case v:
                if not isinstance(v, (int, float)):
                    return False
    return True


def _is_override_protocol_type(val: Mapping[object, object]) -> bool:
    return True


def is_test_protocol(val: object) -> TypeIs[TestProtocol]:
    """Check if a dictionary conforms to the TestProtocol TypedDict.

    Parameters
    ----------
    val : JSON_TYPE
        The dictionary to check.

    Returns
    -------
    bool
        True if the dictionary conforms to the TestProtocol TypedDict, False otherwise.

    """
    if not isinstance(val, Mapping):
        return False
    val = cast("Mapping[object, object]", val)
    match val.get("type"):
        case str(kind) if kind in _PROTOCOL_REQUIRED:
            return _is_special_protocol_type(val, kind)
        case str(kind) if kind == "Override":
            return _is_override_protocol_type(val)
        case _:
            return False


def is_all_test_protocols(val: object) -> TypeIs[Mapping[str, TestProtocol]]:
    """Check if a dictionary conforms to Mapping[str, TestProtocol].

    Parameters
    ----------
    val : JSON_TYPE
        The dictionary to check.

    Returns
    -------
    bool
        True if the dictionary conforms to Mapping[str, TestProtocol], False otherwise.

    """
    if not isinstance(val, Mapping):
        return False
    val = cast("Mapping[object, object]", val)
    return all(is_test_protocol(v) for v in val.values())
