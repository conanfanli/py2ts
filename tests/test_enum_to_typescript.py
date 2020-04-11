from enum import Enum
import unittest

from py2ts.python2ts import enum_to_typescript


class Enum2TsTestCase(unittest.TestCase):
    def test_enum_2_ts(self) -> None:
        class EnumFruit(Enum):
            APPLE = "APPLE"
            ORANGE = "ORANGE"

        assert (
            enum_to_typescript(EnumFruit)
            == """export enum EnumFruit {
  APPLE = 'APPLE',
  ORANGE = 'ORANGE'
}"""
        )
