from datetime import date, datetime
from decimal import Decimal
import unittest

from py2ts.python2ts import python_type_to_typescript


class Enum2TsTestCase(unittest.TestCase):
    def test_python_type_to_typescript(self) -> None:
        assert python_type_to_typescript(str) == "string"
        assert python_type_to_typescript(int) == "number"
        assert python_type_to_typescript(bool) == "boolean"
        assert python_type_to_typescript(float) == "number"
        assert python_type_to_typescript(datetime) == "string"
        assert python_type_to_typescript(date) == "string"
        assert python_type_to_typescript(Decimal) == "string"
        assert python_type_to_typescript(dict) == "{}"
        assert python_type_to_typescript(list) == "Array<any>"
