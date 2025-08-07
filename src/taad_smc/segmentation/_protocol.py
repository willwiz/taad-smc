from collections.abc import Mapping, Sequence
from pprint import pformat

import numpy as np
from pytools.logging.trait import NULL_LOG, ILogger

from .struct import TAADCurve
from .trait import CurveSegment, Protocol, TestProtocol


def create_sawtooth_curve(
    prot: Protocol,
    sample_rate: int,
    *,
    nth: int = 0,
) -> TAADCurve[np.float64, np.intp]:
    """Create a sawtooth curve for testing."""
    half_period = prot["max_strain"] / prot["loading_rate"]
    order = np.array([0, 1, 2], dtype=np.intp)
    time = (order * half_period).astype(np.float64)
    disp = prot["max_strain"] * np.array([0, 1, 0], dtype=np.float64)
    idx = np.rint(time * sample_rate).astype(np.intp)
    return TAADCurve(
        nth=nth,
        idx=idx,
        order=order,
        time=time,
        disp=disp,
        curve=[CurveSegment.STRETCH, CurveSegment.RECOVER],
    )


def create_trapazoid_curve(
    prot: Protocol,
    sample_rate: int,
    *,
    nth: int = 0,
) -> TAADCurve[np.float64, np.intp]:
    """Create a sawtooth curve for testing."""
    duration = prot.get("duration")
    if duration is None:
        msg = "Duration must be provided for trapazoid curve."
        raise ValueError(msg)
    half_period = prot["max_strain"] / prot["loading_rate"]
    order = np.array([0, 1, 2, 3], dtype=np.intp)
    time = np.add.accumulate(np.array([0, half_period, duration, half_period], dtype=np.float64))
    disp = prot["max_strain"] * np.array([0, 1, 1, 0], dtype=np.float64)
    idx = np.rint(time * sample_rate).astype(np.intp)
    return TAADCurve(
        nth=nth,
        idx=idx,
        order=order,
        time=time,
        disp=disp,
        curve=[CurveSegment.STRETCH, CurveSegment.HOLD, CurveSegment.RECOVER],
    )


def create_curve(
    test: TestProtocol,
    *,
    sample_rate: int = 5000,
) -> Sequence[TAADCurve[np.float64, np.intp]]:
    match test["type"]:
        case "Sawtooth":
            return [
                create_sawtooth_curve(test["args"], sample_rate=sample_rate, nth=i)
                for i in range(test["repeat"])
            ]
        case "Trapazoid":
            return [
                create_trapazoid_curve(test["args"], sample_rate=sample_rate, nth=i)
                for i in range(test["repeat"])
            ]


def aligned_curve_indices[F: np.floating, I: np.integer](
    curves: dict[str, Sequence[TAADCurve[F, I]]],
    *,
    start_idx: int = 0,
) -> dict[str, Sequence[TAADCurve[F, I]]]:
    max_idx: int = start_idx
    max_order: int = 1
    max_time: float = 0
    for value in curves.values():
        for curve in value:
            new_idx = (curve.idx + max_idx).astype(curve.idx.dtype)
            curve.idx = new_idx
            new_order = (curve.order + max_order).astype(curve.order.dtype)
            curve.order = new_order
            new_time = (curve.time + max_time).astype(curve.time.dtype)
            curve.time = new_time
            max_idx = new_idx[-1]
            max_order = new_order[-1]
            max_time = new_time[-1]
    return curves


def generate_tags[F: np.floating, I: np.integer](
    curves: Mapping[str, Sequence[TAADCurve[F, I]]],
    *,
    log: ILogger = NULL_LOG,
) -> Sequence[tuple[str, int, str]]:
    """Generate tags for each curve in the protocol."""
    tags = (
        [("Start", 0, "Hold")]
        + [(k, c.nth, m) for k, v in curves.items() for c in v for m in c.curve]
        + [("End", 0, "Hold")]
    )
    log.debug("Curve tags:", pformat(tags, indent=2, sort_dicts=False))
    return tags
