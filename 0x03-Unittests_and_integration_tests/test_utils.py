#!/usr/bin/env python3
"""test_utils.py
Implements a parameterized unit test.
"""
import unittest
from unittest import mock
from unittest.mock import patch
from parameterized import parameterized
from utils import access_nested_map, get_json, memoize


class TestAccessNestedMap(unittest.TestCase):
    """Unit test for `utils.access_nested_map`."""

    @parameterized.expand([
        ({"a": 1}, ("a",), 1),
        ({"a": {"b": 2}}, ("a",), {"b": 2}),
        ({"a": {"b": 2}}, ("a", "b"), 2)
    ])
    def test_access_nested_map(self, nested_map, path, expected):
        """Tests `access_nested_map` method."""
        self.assertEqual(access_nested_map(nested_map, path), expected)

    @parameterized.expand([
        ({}, ("a",)),
        ({"a": 1}, ("a", "b"))
    ])
    def test_access_nested_map_exception(self, nested_map, path):
        """Handles exceptions."""
        with self.assertRaises(KeyError):
            access_nested_map(nested_map, path)


class TestGetJson(unittest.TestCase):
    """Unit test for `get_json` method."""
    @parameterized.expand([
        ("http://example.com", {"payload": True}),
        ("http://holberton.io", {"payload": False})
    ])
    @mock.patch('requests.get')
    def test_get_json(self, test_url, expected, get):
        """Tests `get_json` method."""
        get.return_value.json.return_value = expected
        get.return_value.status_code = 200

        result = get_json(test_url)
        get.assert_called_once_with(test_url)
        self.assertEqual(result, expected)


class TestMemoize(unittest.TestCase):
    """Unit test for `memoize` method."""

    def test_memoize(self):
        """Tests `memoize` method."""
        class TestClass:
            """Test class."""

            def a_method(self):
                """a_method."""
                return 42

            @memoize
            def a_property(self):
                """a_property."""
                return self.a_method()

        test_instance = TestClass()
        # Use patch.object to mock a_method
        with patch.object(test_instance, 'a_method',
                          return_value=42) as mock_a_method:

            # Call a_property twice
            result1 = test_instance.a_property
            result2 = test_instance.a_property

            mock_a_method.assert_called_once()

            self.assertEqual(result1, 42)
            self.assertEqual(result2, 42)


if __name__ == '__main__':
    unittest.main()
