from .exceptions import UnknowFieldType as UnknowFieldType
from dataclasses import Field
from enum import Enum
from typing import Any, Dict, List, Optional, Type

class Undefined: ...

def check_is_subclass(obj: Any, cls: Any) -> Optional[bool]: ...
def is_field_required(field: Field) -> bool: ...

TYPE_MAP: Any

def dataclass2graphene(schema: Any) -> str: ...

class Node:
    is_dataclass: bool = ...
    is_enum: bool = ...
    schema: Any = ...
    def __init__(self, schema: Any) -> None: ...
    @property
    def path(self) -> str: ...
    def to_graphene(self) -> str: ...
    def get_dependencies(self) -> List[Node]: ...

def get_field_dependencies(typing_type: type) -> List[Node]: ...
def python_type_to_graphene(typing_type: type) -> str: ...
def field_to_graphene_field(field: Field) -> str: ...
def enum_to_graphene(enum_class: Type[Enum]) -> str: ...
def traverse(node: Node, visited: Dict[str, Node]) -> Any: ...
def schemas2graphene(schemas: List) -> Dict[str, Node]: ...