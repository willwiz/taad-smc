from pprint import pformat
from typing import TYPE_CHECKING

import numpy as np
from pytools.result import Err, Ok

from pwlsplit.plot import plot_segmentation_part
from pwlsplit.segment.split import adjust_segmentation

if TYPE_CHECKING:
    from pathlib import Path

    from pytools.logging.trait import ILogger

    from pwlsplit.trait import PreppedData, Segmentation

    from ._types import PROTOCOL_MAP


def segmentation_loop[F: np.floating, I: np.integer](
    protocol_map: PROTOCOL_MAP,
    segmentation: Segmentation[F, I],
    prepped_data: PreppedData[F],
    *,
    log: ILogger,
    fparent: Path | None = None,
) -> Ok[Segmentation[F, I]] | Err:
    for k, (prot, cycles) in enumerate(protocol_map.items()):
        log.brief(f"Working on Protocol: {prot}")
        cycle_idx = sorted({c for cycle in cycles.values() for c in cycle})
        match adjust_segmentation(prepped_data, segmentation, cycle_idx):
            case Ok(segmentation):
                log.debug(pformat(segmentation.idx, sort_dicts=False))
                if fparent is not None:
                    fig_name = f"FindPeaks_{k}_{prot}_segmentation.png"
                    plot_segmentation_part(
                        prepped_data, segmentation, cycle_idx, fout=fparent / fig_name
                    )
            case Err(e):
                return Err(e)
    return Ok(segmentation)
