[![CircleCI](https://circleci.com/gh/conanfanli/py2ts.svg?style=svg)](https://circleci.com/gh/conanfanli/py2ts)
[![codecov](https://codecov.io/gh/conanfanli/py2ts/branch/master/graph/badge.svg)](https://codecov.io/gh/conanfanli/py2ts)

# py2ts
Covert Python [dataclass](https://docs.python.org/3/library/dataclasses.html) and [Enum](https://docs.python.org/3/library/enum.html) to TypeScript interface.

# Mapping of Scalar Types
```python
assert python_type_to_typescript(str) == "string"
assert python_type_to_typescript(int) == "number"
assert python_type_to_typescript(bool) == "boolean"
assert python_type_to_typescript(float) == "number"
assert python_type_to_typescript(datetime) == "string"
assert python_type_to_typescript(date) == "string"
assert python_type_to_typescript(Decimal) == "string"
assert python_type_to_typescript(dict) == "{}"
assert python_type_to_typescript(list) == "Array<any>"
```

# Usage
Create a schema with Python `dataclass`:

```python
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
    nested_list_field: List[NestedSchema]

blocks = []
for path, node in schemas2typescript([ComplexSchema]).items():
    blocks.append(node.to_typescript())

print("\n".join(blocks))
```
The output is:
```typescript
export enum EnumFruit {
  APPLE = 'APPLE',
  ORANGE = 'ORANGE'
}
export interface NestedSchema {
  string_field: string;
  nullable_datetime_field: string | null;
  recursively_nested_field: NestedSchema | null;
}
export interface ComplexSchema {
  nullable_int_field: number | null;
  nullable_decimal_field: number | null;
  nullable_enum_field: EnumFruit | null;
  nullable_nested_field: NestedSchema | null;
  nested_list_field: Array<NestedSchema>;
}
```

# Generate service registry
Dependency: [ripgrep](https://github.com/BurntSushi/ripgrep)

Generate boilerplate service registry code.

## Usage
`python -m py2ts.generate_service_registry > service_registery.py`

## How it works
The command assumes that any classes named `XXXService` should be included in the service registry.
For example:
```python
class TestService:
    pass
```

will generate the following code:
```python
# Generated code. DO NOT EDIT!

from dataclasses import dataclass

from tests.test_generate_service_registr import TestService


@dataclass
class ServiceRegistry:
    test_service: TestService = TestService()

service_registry = ServiceRegistry()
```
