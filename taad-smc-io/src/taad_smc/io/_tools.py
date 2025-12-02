from typing import TYPE_CHECKING, TypeIs

from pwlsplit.curve.validator import validate_curve_segment
from pwlsplit.trait import SegmentDict
from pytools.result import Err, Ok

if TYPE_CHECKING:
    from collections.abc import Mapping, Sequence

    from ._types import TEST_NAMES, TestProtocol

__all__ = ["construct_protocol", "validate_protocol"]


_TEST_DICTS: dict[TEST_NAMES, set[str]] = {
    "Sawtooth": {"max_strain", "duration"},
    "Trapazoid": {"max_strain", "loading", "unloading"},
    "Hold": set(),
    "Slack": {"max_strain", "duration", "loading"},
    "Override": set(),
}


def _is_valid_curve(curve: object) -> TypeIs[TEST_NAMES]:
    return curve in _TEST_DICTS


def _is_list(obj: object) -> TypeIs[list[object]]:
    return isinstance(obj, list)


def _validate_overrided_segment(test: Mapping[str, object]) -> Ok[None] | Err:
    if not _is_list(segments := test.get("segments")):
        return Err(TypeError("'segments' must be a list of segment dictionaries."))
    for s in segments:
        match validate_curve_segment(s):
            case Err(e):
                return Err(e)
            case Ok(None):
                return Ok(None)
    return Ok(None)


def validate_protocol(test: Mapping[str, object]) -> Ok[None] | Err:
    match test.get("type"):
        case None:
            return Err(LookupError("Missing 'type' in test protocol."))
        case test_curve if _is_valid_curve(test_curve):
            pass
        case test_curve:
            msg = f"Unknown test type '{test_curve}'."
            return Err(LookupError(msg))
    if test_curve == "Override":
        match _validate_overrided_segment(test):
            case Err(e):
                return Err(e)
            case Ok(None):
                return Ok(None)
    msg = ""
    for k in _TEST_DICTS[test_curve]:
        if k not in test:
            msg += f"Missing required attribute '{k}' for test type '{test_curve}'.\n"
    if msg:
        return Err(LookupError(msg))
    return Ok(None)


def _construct_sawtooth_segments(test: TestProtocol) -> Ok[list[SegmentDict]] | Err:
    match test.get("max_strain"):
        case None:
            return Err(LookupError("Missing 'max_strain' for Sawtooth protocol."))
        case delta:
            pass
    match test.get("duration"):
        case None:
            return Err(LookupError("Missing 'duration' for Sawtooth protocol."))
        case duration:
            pass
    if delta > 0:
        return Ok(
            [
                SegmentDict(curve="STRETCH", delta=delta, time=duration),
                SegmentDict(curve="RECOVER", delta=-delta, time=duration),
            ]
        )
    return Ok(
        [
            SegmentDict(curve="RECOVER", delta=delta, time=duration),
            SegmentDict(curve="STRETCH", delta=-delta, time=duration),
        ]
    )


def _construct_trapazoid_segments(
    test: TestProtocol,
) -> Ok[list[SegmentDict]] | Err:
    match test.get("max_strain"):
        case None:
            return Err(LookupError("Missing 'max_strain' for Trapazoid protocol."))
        case delta:
            pass
    match test.get("loading"):
        case None:
            return Err(LookupError("Missing 'loading' for Trapazoid protocol."))
        case loading:
            pass
    match test.get("unloading"):
        case None:
            return Err(LookupError("Missing 'unloading' for Trapazoid protocol."))
        case unloading:
            pass
    if delta > 0:
        return Ok(
            [
                SegmentDict(curve="STRETCH", delta=delta, time=loading),
                SegmentDict(curve="HOLD"),
                SegmentDict(curve="RECOVER", delta=-delta, time=unloading),
            ]
        )
    return Ok(
        [
            SegmentDict(curve="RECOVER", delta=delta, time=loading),
            SegmentDict(curve="HOLD"),
            SegmentDict(curve="STRETCH", delta=-delta, time=unloading),
        ]
    )


def _construct_hold_segments(_test: TestProtocol) -> Ok[list[SegmentDict]] | Err:
    return Ok([SegmentDict(curve="HOLD")])


def _construct_slack_segments(test: TestProtocol) -> Ok[list[SegmentDict]] | Err:
    match test.get("max_strain"):
        case None:
            return Err(LookupError("Missing 'max_strain' for Slack protocol."))
        case delta:
            pass
    match test.get("loading"):
        case None:
            return Err(LookupError("Missing 'loading' for Slack protocol."))
        case loading:
            pass
    if delta > 0:
        return Ok(
            [
                SegmentDict(curve="STRETCH", delta=delta, time=loading),
                SegmentDict(curve="HOLD"),
                SegmentDict(curve="RECOVER", delta=-delta, time=loading),
            ]
        )
    return Ok(
        [
            SegmentDict(curve="RECOVER", delta=delta, time=loading),
            SegmentDict(curve="HOLD"),
            SegmentDict(curve="STRETCH", delta=-delta, time=loading),
        ]
    )


def _construct_override_segments(test: TestProtocol) -> Ok[Sequence[SegmentDict]] | Err:
    match test.get("segments"):
        case None:
            return Err(LookupError("Missing 'segments' for Override protocol."))
        case segments:
            pass
    for s in segments:
        match validate_curve_segment(s):
            case Err(e):
                return Err(e)
            case Ok(None):
                pass
    return Ok(segments)


def construct_protocol(
    test: TestProtocol,
) -> Ok[Mapping[str, Sequence[SegmentDict]]] | Err:
    repeat = test.get("repeat", 1)
    match test["type"]:
        case "Sawtooth":
            res = _construct_sawtooth_segments(test)
        case "Trapazoid":
            res = _construct_trapazoid_segments(test)
        case "Hold":
            res = _construct_hold_segments(test)
        case "Slack":
            res = _construct_slack_segments(test)
        case "Override":
            res = _construct_override_segments(test)
    match res:
        case Ok(segments):
            return Ok({f"cycle_{i}": segments for i in range(repeat)})
        case Err(e):
            return Err(e)
