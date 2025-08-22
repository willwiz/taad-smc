import json
from collections.abc import Mapping
from pathlib import Path

from .trait import TestProtocol


def import_test_protocol(file: Path) -> Mapping[str, TestProtocol]:
    meta_data_file = file.parent / "protocol.json"
    with meta_data_file.open("r") as f:
        meta_data: dict[str, TestProtocol] = json.load(f)
    return meta_data
