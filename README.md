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
```
