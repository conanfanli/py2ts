from datetime import date, datetime
from decimal import Decimal
import unittest

from py2ts.python2graphene import python_type_to_graphene


class GrapheneTypeTestCase(unittest.TestCase):
    def test_python_type_to_typescript(self) -> None:
        assert python_type_to_graphene(str) == "String"
        assert python_type_to_graphene(int) == "Int"
        assert python_type_to_graphene(bool) == "Boolean"
        assert python_type_to_graphene(float) == "Float"
        assert python_type_to_graphene(datetime) == "String"
        assert python_type_to_graphene(date) == "String"
        assert python_type_to_graphene(Decimal) == "String"
        assert python_type_to_graphene(dict) == "JSONString"
        assert python_type_to_graphene(list) == "List"
