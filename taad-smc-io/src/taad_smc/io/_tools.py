from typing import TYPE_CHECKING, Literal

from pwlsplit.trait import SegmentDict
from pytools.result import Err, Ok

if TYPE_CHECKING:
    from collections.abc import Sequence

    from taad_smc.io.trait import TestProtocol

_TEST_DICTS: dict[Literal["Sawtooth", "Trapazoid", "Hold", "Slack"], set[str]] = {
    "Sawtooth": {"repeat", "max_strain", "duration"},
    "Trapazoid": {"repeat", "max_strain", "loading", "unloading"},
    "Hold": {"repeat"},
    "Slack": {"repeat", "max_strain", "duration", "loading"},
}


def validate_protocol(test: TestProtocol) -> Ok[None] | Err:
    match _TEST_DICTS.get(test["type"]):
        case None:
            msg = f"Unknown test type '{test['type']}'."
            return Err(LookupError(msg))
        case required_attributes:
            msg = ""
    for k in required_attributes:
        if k not in test:
            msg += f"Missing required attribute '{k}' for test type '{test['type']}'.\n"
    if msg:
        return Err(LookupError(msg))
    return Ok(None)


def _construct_sawtooth_segments(test: TestProtocol) -> Ok[Sequence[SegmentDict]] | Err:
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
                SegmentDict(curve="STRETCH", delta=delta, duration=duration),
                SegmentDict(curve="RECOVER", delta=-delta, duration=duration),
            ]
        )
    return Ok(
        [
            SegmentDict(curve="RECOVER", delta=delta, duration=duration),
            SegmentDict(curve="STRETCH", delta=-delta, duration=duration),
        ]
    )


def _construct_trapazoid_segments(
    test: TestProtocol,
) -> Ok[Sequence[SegmentDict]] | Err:
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
                SegmentDict(curve="STRETCH", delta=delta, duration=loading),
                SegmentDict(curve="HOLD"),
                SegmentDict(curve="RECOVER", delta=-delta, duration=unloading),
            ]
        )
    return Ok(
        [
            SegmentDict(curve="RECOVER", delta=delta, duration=loading),
            SegmentDict(curve="HOLD"),
            SegmentDict(curve="STRETCH", delta=-delta, duration=unloading),
        ]
    )


def _construct_hold_segments(_test: TestProtocol) -> Ok[Sequence[SegmentDict]] | Err:
    return Ok([SegmentDict(curve="HOLD")])


def _construct_slack_segments(test: TestProtocol) -> Ok[Sequence[SegmentDict]] | Err:
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
                SegmentDict(curve="STRETCH", delta=delta, duration=loading),
                SegmentDict(curve="HOLD"),
                SegmentDict(curve="RECOVER", delta=-delta, duration=loading),
            ]
        )
    return Ok(
        [
            SegmentDict(curve="RECOVER", delta=delta, duration=loading),
            SegmentDict(curve="HOLD"),
            SegmentDict(curve="STRETCH", delta=-delta, duration=loading),
        ]
    )


def construct_protocol(test: TestProtocol) -> Ok[Sequence[SegmentDict]] | Err:
    match test["type"]:
        case "Sawtooth":
            return _construct_sawtooth_segments(test)
        case "Trapazoid":
            return _construct_trapazoid_segments(test)
        case "Hold":
            return _construct_hold_segments(test)
        case "Slack":
            return _construct_slack_segments(test)
