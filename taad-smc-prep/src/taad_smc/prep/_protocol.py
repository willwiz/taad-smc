from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from collections.abc import Mapping

    from taad_smc.io.types import PROTOCOL_NAMES, TestProtocol

    from ._types import ProtocolGenerator


def _saw(s: float, r: float) -> TestProtocol:
    return {
        "type": "Sawtooth",
        "repeat": 3,
        "max_strain": round(s, 2),
        "duration": round(s / r, 2),
    }


def gen_cycling_protocols(strain: float, /) -> Mapping[str, TestProtocol]:
    """Generate cycling protocols for testing.

    Parameters
    ----------
    strain : float
        The maximum strain to be used in the protocols.

    Returns
    -------
    Mapping[str, TestProtocol]
        JSON for TestProtocol definitions.

    """
    precondition: TestProtocol = {
        "type": "Sawtooth",
        "repeat": 10,
        "max_strain": strain,
        "duration": 0.5,
    }
    # protocol: Mapping[str, TestProtocol] = {
    #     "START": {"type": "Hold"},
    #     "Zeroing": {"type": "Trapazoid", "max_strain": -0.05, "loading": 10, "unloading": 10},
    #     "Hold_Z": {"type": "Hold"},
    #     "Preconditioning": precondition,
    #     "Hold_P": {"type": "Hold"},
    #     "Saw_Slow_30": _saw(strain, strain / 12.5),
    #     "Hold_S30": {"type": "Hold"},
    #     "Saw_Slow_20": _saw(2 / 3 * strain, strain / 12.5),
    #     "Hold_S20": {"type": "Hold"},
    #     "Saw_Slow_10": _saw(1 / 3 * strain, strain / 12.5),
    #     "Hold_S10": {"type": "Hold"},
    #     "Relax_Slow": {"type": "Trapazoid", "max_strain": strain, "loading": 12.5, "unloading": 5},
    #     "Hold_SR": {"type": "Hold"},
    #     "Saw_Mid_30": _saw(strain, strain / 2.5),
    #     "Hold_M30": {"type": "Hold"},
    #     "Saw_Mid_20": _saw(2 / 3 * strain, strain / 2.5),
    #     "Hold_M20": {"type": "Hold"},
    #     "Saw_Mid_10": _saw(1 / 3 * strain, strain / 2.5),
    #     "Hold_M10": {"type": "Hold"},
    #     "Relax_Mid": {"type": "Trapazoid", "max_strain": strain, "loading": 2.5, "unloading": 5},
    #     "Hold_MR": {"type": "Hold"},
    #     "Saw_Fast_30": _saw(strain, strain / 0.5),
    #     "Hold_F30": {"type": "Hold"},
    #     "Saw_Fast_20": _saw(2 / 3 * strain, strain / 0.5),
    #     "Hold_F20": {"type": "Hold"},
    #     "Saw_Fast_10": _saw(1 / 3 * strain, strain / 0.5),
    #     "Hold_F10": {"type": "Hold"},
    #     "Relax_Fast": {"type": "Trapazoid", "max_strain": strain, "loading": 0.5, "unloading": 5},
    #     "END": {"type": "Hold"},
    # }
    protocol: Mapping[str, TestProtocol] = {
        "START": {"type": "Hold"},
        "Zeroing": {"type": "Trapazoid", "max_strain": -0.05, "loading": 10, "unloading": 10},
        "Hold_Z": {"type": "Hold"},
        "Preconditioning": precondition,
        "Hold_P": {"type": "Hold"},
        "Saw_Slow_30": _saw(strain, strain / 12.5),
        "Hold_S30": {"type": "Hold"},
        "Saw_Slow_20": _saw(2 / 3 * strain, strain / 12.5),
        "Hold_S20": {"type": "Hold"},
        "Saw_Slow_10": _saw(1 / 3 * strain, strain / 12.5),
        "Hold_S10": {"type": "Hold"},
        "Relax_Slow": {"type": "Trapazoid", "max_strain": strain, "loading": 12.5, "unloading": 5},
        "Hold_SR": {"type": "Hold"},
        "Saw_Mid_30": _saw(strain, strain / 2.5),
        "Hold_M30": {"type": "Hold"},
        "Saw_Mid_20": _saw(2 / 3 * strain, strain / 2.5),
        "Hold_M20": {"type": "Hold"},
        "Saw_Mid_10": _saw(1 / 3 * strain, strain / 2.5),
        "Hold_M10": {"type": "Hold"},
        "Relax_Mid": {"type": "Trapazoid", "max_strain": strain, "loading": 2.5, "unloading": 5},
        "Hold_MR": {"type": "Hold"},
        "Saw_Fast_30": _saw(strain, strain / 0.5),
        "Hold_F30": {"type": "Hold"},
        "Saw_Fast_20": _saw(2 / 3 * strain, strain / 0.5),
        "Hold_F20": {"type": "Hold"},
        "Saw_Fast_10": _saw(1 / 3 * strain, strain / 0.5),
        "Hold_F10": {"type": "Hold"},
        "Relax_Fast": {"type": "Trapazoid", "max_strain": strain, "loading": 0.5, "unloading": 5},
        "END": {"type": "Hold"},
    }
    return protocol


def gen_activation_protocols(strain: float, /) -> Mapping[str, TestProtocol]:
    """Generate activation protocols for testing.

    Parameters
    ----------
    strain : float
        The maximum strain to be used in the protocols.

    Returns
    -------
    Mapping[str, TestProtocol]
        JSON for TestProtocol definitions.

    """
    return {
        "START": {"type": "Hold"},
        "Relax_Mid": {"type": "Trapazoid", "max_strain": strain, "loading": 2.5, "unloading": 5},
        "END": {"type": "Hold"},
    }


def gen_rest_protocols(_strain: float, /) -> Mapping[str, TestProtocol]:
    """Generate rest protocols for testing.

    Returns
    -------
    Mapping[str, TestProtocol]
        JSON for TestProtocol definitions.

    """
    return {"REST": {"type": "Hold"}}


def gen_preconditioning_protocols(strain: float, /) -> Mapping[str, TestProtocol]:
    """Generate preconditioning protocols for testing.

    Parameters
    ----------
    strain : float
        The maximum strain to be used in the protocols.

    Returns
    -------
    Mapping[str, TestProtocol]
        JSON for TestProtocol definitions.

    """

    def precondition(d: float) -> TestProtocol:
        return {
            "type": "Sawtooth",
            "repeat": 5,
            "max_strain": strain,
            "duration": d,
        }

    return {
        "START": {"type": "Hold"},
        "Preconditioning_Saw_Fast_30": precondition(0.5),
        "Hold_PF": {"type": "Hold"},
        "Preconditioning_Saw_Slow_30": precondition(12.5),
        "Hold_PS": {"type": "Hold"},
        "Preconditioning_Relax_Fast": precondition(0.5),
        "END": {"type": "Hold"},
    }


PROTOCOL_GENERATORS: Mapping[PROTOCOL_NAMES, ProtocolGenerator] = {
    "activation": gen_activation_protocols,
    "activated": gen_cycling_protocols,
    "deactivation": gen_activation_protocols,
    "deactivated": gen_cycling_protocols,
    "initial": gen_cycling_protocols,
    "preconditioning_start": gen_preconditioning_protocols,
    "preconditioning_activated": gen_preconditioning_protocols,
    "preconditioning_deactivated": gen_preconditioning_protocols,
    "rest_start": gen_rest_protocols,
    "rest_end": gen_rest_protocols,
}
