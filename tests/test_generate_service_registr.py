import unittest

from py2ts.generate_service_registry import (
    get_class_module_map,
    get_service_registry_code,
)


class TestService:
    pass


class GenerateServiceRegistryTestCase(unittest.TestCase):
    def test_generate_service_registry(self):
        assert (
            get_service_registry_code(get_class_module_map())
            == """\n# Generated code. DO NOT EDIT!

from dataclasses import dataclass

from tests.test_generate_service_registr import TestService


@dataclass
class ServiceRegistry:
    test_service: TestService = TestService()

service_registry = ServiceRegistry()
"""
        )
