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


def check_is_subclass(obj, cls) -> Optional[bool]:
    """Call issubclass without raising exceptions."""
    try:
        return issubclass(obj, cls)
    except TypeError:
        return None


def is_field_required(field: Field) -> bool:
    return field.default is MISSING


TYPE_MAP = {
    str: "string",
    bool: "boolean",
    int: "number",
    Decimal: "string",
    float: "number",
    datetime.datetime: "string",
    datetime.date: "string",
    dict: "{}",
    Any: "any",
    list: "Array<any>",
}


def dataclass2interface(schema) -> str:
    interface_body = "\n".join(
        [
            f"  {field.name}: {field_to_typescript(field)}"
            if is_field_required(field)
            else f"  {field.name}?: {field_to_typescript(field)}"
            for field in dataclasses.fields(schema)
        ]
    )
    return "export interface {} {{\n{}\n}}".format(schema.__name__, interface_body)


class Node:
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

    def to_typescript(self) -> str:
        if is_dataclass(self.schema):
            return dataclass2interface(self.schema)

        return enum_to_typescript(self.schema)

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
        return self.to_typescript()


def get_field_dependencies(typing_type: type) -> List[Node]:
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
        args = getattr(typing_type, "__args__")
        return [
            Node(arg)
            for arg in args
            if is_dataclass(arg) or check_is_subclass(arg, Enum)
        ]

    return []


def python_type_to_typescript(typing_type: type) -> str:
    """
    >>> python_type_to_typescript(str)
    'string'
    """
    if typing_type in TYPE_MAP:
        return TYPE_MAP[typing_type]

    if typing_type is Undefined:
        return "undefined"

    # Nested type
    if is_dataclass(typing_type):
        return typing_type.__name__

    if getattr(typing_type, "__name__", None) == "NoneType":
        return "null"

    if getattr(typing_type, "__origin__", None) in [list, List]:
        args = getattr(typing_type, "__args__")
        return "Array<{}>".format(python_type_to_typescript(args[0]))

    if getattr(typing_type, "__origin__", None) == Union:
        args = getattr(typing_type, "__args__")
        return " | ".join(python_type_to_typescript(arg) for arg in args)

    if isinstance(typing_type, ForwardRef):
        return typing_type.__forward_arg__

    if isinstance(typing_type, type) and issubclass(typing_type, Enum):
        return typing_type.__name__

    raise UnknowFieldType(f"Unknow type {typing_type}")


def field_to_typescript(field: Field) -> str:
    try:
        return python_type_to_typescript(field.type) + ";"
    except UnknowFieldType as e:
        raise UnknowFieldType(f"{field.name}: {e}")


def enum_to_typescript(enum_class: Type[Enum]) -> str:
    body = ",\n".join(f"  {member.name} = '{member.name}'" for member in enum_class)
    return "export enum {} {{\n{}\n}}".format(enum_class.__name__, body)


def traverse(node: Node, visited: Dict[str, Node]):
    for dep in node.get_dependencies():
        if dep.path not in visited:
            traverse(dep, visited)

    visited[node.path] = node


def schemas2typescript(schemas: List) -> Dict[str, Node]:
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
