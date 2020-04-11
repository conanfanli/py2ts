from dataclasses import dataclass
from enum import Enum
from typing import List, Optional
import unittest

from py2ts.python2ts import schemas2typescript


class EnumFruit(Enum):
    APPLE = "APPLE"
    ORANGE = "ORANGE"


@dataclass
class ComplexSchema:
    nullable_int_field: Optional[int]
    nullable_decimal_field: Optional[int]
    nullable_enum_fields: Optional[EnumFruit]


class Enum2TsTestCase(unittest.TestCase):
    @property
    def snapshot_path(self) -> str:
        prefix, _ = __file__.rsplit(".", maxsplit=1)
        return f"{prefix}__snapshot.ts"

    def read_snapshot(self) -> str:
        with open(self.snapshot_path) as f:
            return f.read().strip()

    def updateSnapshot(self, blocks: List[str]) -> None:
        """Use this when updating snapshot."""
        with open(self.snapshot_path, "w") as f:
            print("\n".join(blocks), file=f)

    def test_schemas2typescript(self) -> None:
        blocks = []
        for path, node in schemas2typescript([ComplexSchema]).items():
            blocks.append(node.to_typescript())

        # self.updateSnapshot(blocks)
        assert "\n".join(blocks) == self.read_snapshot()
