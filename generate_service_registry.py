import re
import subprocess
from typing import Dict


class RipgrepError(Exception):
    pass


def camel_to_snake(name: str) -> str:
    name = re.sub("(.)([A-Z][a-z]+)", r"\1_\2", name)
    return re.sub("([a-z0-9])([A-Z])", r"\1_\2", name).lower()


def get_service_registry_code(class_module_map: Dict[str, str]) -> str:
    """Return generated code for service registry."""
    imports = []
    services = []
    for service_name, path in class_module_map.items():
        imports.append(f"from {path} import {service_name}")
        services.append(
            f"{camel_to_snake(service_name)}: {service_name} = {service_name}()"
        )

    imports_code = "\n".join(imports)
    services_code = "\n    ".join(services)
    return f"""
# Generated code. DO NOT EDIT!

from dataclasses import dataclass

{imports_code}


@dataclass
class ServiceRegistry:
    {services_code}

service_registry = ServiceRegistry()
"""


def get_class_module_map() -> Dict[str, str]:
    class_module_map = {}
    result = subprocess.run(
        f"rg '^class \\w+Service[\\(:]'", shell=True, capture_output=True,
    )

    # Command successful
    if result.returncode == 0:
        # E.g., ['smartcat/services.py:class TrainingDataSetService:', 'smartcat/services.py:class SmartCatService:']
        outputs = result.stdout.decode("utf-8").strip().split("\n")
        print("Output of rg:", outputs)
        for output in outputs:
            # E.g., smartcat/services.py-class SmartCatService:
            file_path, class_name = output.rstrip(":").split(":class ")
            module = file_path.split(".py")[0].replace("/", ".")
            assert class_name not in class_module_map, f"Found duplicate {class_name}"
            class_module_map[class_name] = module

    elif result.returncode > 1:
        # resultcode of 1 means no matches were found
        raise RipgrepError(
            "Got code: {result.returncode} with message: {result.stderr!r}"
        )

    return class_module_map


if __name__ == "__main__":
    code = get_service_registry_code(get_class_module_map())
    print(code)
    with open("registries/service_registry.py", "w") as f:
        f.write(code)
