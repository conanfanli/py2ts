from collections import OrderedDict
import dataclasses
from dataclasses import MISSING, Field, is_dataclass
import datetime
from decimal import Decimal
from enum import Enum
from typing import Any, Dict, List, Optional, Type, Union
from typing import ForwardRef  # type: ignore

from .exceptions import UnknowFieldType


class Undefined:
    pass


def parse_union_type(typing_type: type) -> str:
    """
    typing_type: str, int, typing.Union[int, str] ...
    """
    assert getattr(typing_type, "__origin__", None) == Union

    non_null_types = [
        ut
        for ut in typing_type.__args__  # type: ignore
        if getattr(ut, "__name__", None) != "NoneType"
    ]
    # When there's only 1 type in Union or Option[SomeType]
    if len(non_null_types) == 1:
        return "".join(
            python_type_to_graphene(union_type) for union_type in non_null_types
        )
    else:
        union_class_name = "Union" + "".join(
            [ut.__name__.capitalize() for ut in non_null_types]
        )
        return union_class_name


def check_is_subclass(obj, cls) -> Optional[bool]:
    """Call issubclass without raising exceptions."""
    try:
        return issubclass(obj, cls)
    except TypeError:
        return None


def is_field_required(field: Field) -> bool:
    # If field is a Unioned field with None being in the union
    field_type = field.type
    if getattr(field_type, "__origin__", None) == Union:
        args = field_type.__args__
        for arg in args:
            if getattr(arg, "__name__", None) == "NoneType":
                return False

    # If default value is not provided, field is required
    if field.default is MISSING:
        return True
    else:
        return False


TYPE_MAP = {
    str: "graphene.String",
    bool: "graphene.Boolean",
    int: "graphene.Int",
    Decimal: "graphene.String",
    float: "graphene.Float",
    datetime.datetime: "graphene.String",
    datetime.date: "graphene.String",
    dict: "graphene.ObjectType",
    Any: "graphene.ObjectType",
    list: "graphene.List",
}


def dataclass2graphene(schema) -> str:
    lines = []
    for field in dataclasses.fields(schema):
        if is_field_required(field):
            lines.append(f"    {field.name} = {field_to_graphene_field(field)}")
        else:
            lines.append(f"    {field.name} = {field_to_graphene_field(field)}")

    class_body = "\n".join(lines)
    return f"class {schema.__name__}(graphene.ObjectType):\n{class_body}\n"


class Node:
    """Represent a type that is a dataclass, enum"""

    def __init__(self, schema) -> None:
        if is_dataclass(schema):
            self.is_dataclass = True
            self.is_enum = False
        elif check_is_subclass(schema, Enum):
            self.is_dataclass = False
            self.is_enum = True
        else:
            raise Exception(f"{schema} is neither Enum or dataclass")

        self.schema = schema

    @property
    def path(self) -> str:
        return f"{self.schema.__module__}.{self.schema.__name__}"

    def to_graphene(self) -> str:
        if is_dataclass(self.schema):
            return dataclass2graphene(self.schema)

        return enum_to_graphene(self.schema)

    def get_dependencies(self) -> List["Node"]:
        deps: List[Node] = []
        if self.is_dataclass:
            for field in dataclasses.fields(self.schema):
                deps += get_field_dependencies(field.type)
        else:
            # Naively handle Enum dependencies
            deps = []

        return deps

    def __repr__(self) -> str:
        return self.to_graphene()


def get_field_dependencies(typing_type: type) -> List[Node]:
    """Given a field type, return the list of nodes it depends on."""
    if is_dataclass(typing_type) or check_is_subclass(typing_type, Enum):
        return [Node(typing_type)]

    if getattr(typing_type, "__origin__", None) in [list, List]:
        args = getattr(typing_type, "__args__")
        try:
            return (
                [Node(args[0])]
                if is_dataclass(args[0]) or check_is_subclass(args[0], Enum)
                else get_field_dependencies(args[0])
            )
        except TypeError as e:
            raise Exception(f"Type is: {typing_type}") from e

    if getattr(typing_type, "__origin__", None) == Union:
        # Find nested types by filtering for dataclasses and enums
        nested_types = [
            Node(arg)
            for arg in typing_type.__args__  # type: ignore
            if is_dataclass(arg) or check_is_subclass(arg, Enum)
        ]
        return nested_types

    return []


def python_type_to_graphene(typing_type: type) -> str:
    """
    Convert a python type to graphene type.
    >>> python_type_to_graphene(str)
    'graphene.String'
    """
    if typing_type in TYPE_MAP:
        return TYPE_MAP[typing_type]

    if typing_type is Undefined:
        return "undefined"

    # Nested type
    if is_dataclass(typing_type):
        return typing_type.__name__

    # if getattr(typing_type, "__name__", None) == "NoneType":
    #     return "null"

    if getattr(typing_type, "__origin__", None) in [list, List]:
        args = getattr(typing_type, "__args__")
        return "graphene.List({})".format(python_type_to_graphene(args[0]))

    if getattr(typing_type, "__origin__", None) == Union:
        return parse_union_type(typing_type)
    #             return f"""
    # class {union_class_name}:
    #     class Meta:
    #         pass
    # """

    if isinstance(typing_type, ForwardRef):
        return typing_type.__forward_arg__

    if isinstance(typing_type, type) and issubclass(typing_type, Enum):
        return typing_type.__name__

    raise UnknowFieldType(f"Unknow type {typing_type}")


def field_to_graphene_field(field: Field) -> str:
    """Wrap field with graphene.Field"""
    try:
        if is_field_required(field):
            return (
                f"graphene.Field({python_type_to_graphene(field.type)}, required=True)"
            )
        else:
            return (
                f"graphene.Field({python_type_to_graphene(field.type)}, required=False)"
            )
    except UnknowFieldType as e:
        raise UnknowFieldType(f"{field.name}: {e}")


def enum_to_graphene(enum_class: Type[Enum]) -> str:
    body = "\n".join(f"  {member.name} = '{member.name}'" for member in enum_class)
    return "class {}(graphene.Enum):\n{}\n".format(enum_class.__name__, body)


def traverse(node: Node, visited: Dict[str, Node]):
    for dep in node.get_dependencies():
        if dep.path not in visited:
            traverse(dep, visited)

    visited[node.path] = node


def schemas2graphene(schemas: List) -> Dict[str, Node]:
    """
    Args:
        schemas: A list of dataclass schemas or Enum
    interfaces.
    """
    graph: Dict[str, Node] = OrderedDict()
    for schema in schemas:
        node = Node(schema)
        traverse(node, graph)

    return graph
