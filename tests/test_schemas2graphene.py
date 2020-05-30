from dataclasses import dataclass
from datetime import datetime
from enum import Enum
from typing import List, Optional, Union
import unittest

from py2ts.python2graphene import schemas2graphene


class EnumFruit(Enum):
    APPLE = "APPLE"
    ORANGE = "ORANGE"


@dataclass
class NestedSchema:
    string_field: str
    nullable_datetime_field: Optional[datetime]
    recursively_nested_field: Optional["NestedSchema"]


@dataclass
class ComplexSchema:
    nullable_int_field: Optional[int]
    nullable_decimal_field: Optional[int]
    nullable_enum_field: Optional[EnumFruit]
    nullable_nested_field: Optional[NestedSchema]
    union_field: Union[NestedSchema, int, str]
    nested_list_field: List[NestedSchema]


class Enum2TsTestCase(unittest.TestCase):
    @property
    def snapshot_path(self) -> str:
        prefix, _ = __file__.rsplit(".", maxsplit=1)
        return f"{prefix}__snapshot.py"

    def read_snapshot(self) -> str:
        with open(self.snapshot_path) as f:
            return f.read().strip()

    def updateSnapshot(self, blocks: List[str]) -> None:
        """Use this when updating snapshot."""
        with open(self.snapshot_path, "w") as f:
            print("\n".join(blocks), file=f)

    def test_schemas2typescript(self) -> None:
        blocks = []
        for path, node in schemas2graphene([ComplexSchema]).items():
            blocks.append(node.to_graphene())

        # self.updateSnapshot(blocks)
        assert "\n".join(blocks) == self.read_snapshot()
