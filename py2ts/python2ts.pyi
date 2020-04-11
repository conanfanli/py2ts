from .exceptions import UnknowFieldType as UnknowFieldType
from dataclasses import Field
from enum import Enum
from typing import Any, Dict, List, Type

class Undefined: ...

def is_subclass(obj: Any, cls: Any): ...
def is_field_required(field: Field) -> bool: ...

TYPE_MAP: Any

def dataclass2interface(schema: Any) -> str: ...

class Node:
    is_dataclass: bool = ...
    is_enum: bool = ...
    schema: Any = ...
    def __init__(self, schema: Any) -> None: ...
    @property
    def path(self) -> str: ...
    def to_typescript(self) -> str: ...
    def get_dependencies(self) -> List[Node]: ...

def get_field_dependencies(typing_type: type) -> List[Node]: ...
def python_type_to_typescript(typing_type: type) -> str: ...
def field_to_typescript(field: Field) -> str: ...
def enum_to_typescript(enum_class: Type[Enum]) -> str: ...
def traverse(node: Node, visited: Dict[str, Node]) -> Any: ...
def schemas2typescript(schemas: List) -> Dict[str, Node]: ...