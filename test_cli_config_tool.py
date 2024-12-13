import pytest
import json
from main import json_to_custom_config

def test_simple_key_value():
    input_json = {"key": "value"}
    expected_output = 'let key = @"value";'
    assert json_to_custom_config(input_json) == expected_output

def test_number_value():
    input_json = {"number": 42}
    expected_output = 'let number = 42;'
    assert json_to_custom_config(input_json) == expected_output

def test_array_value():
    input_json = {"list": [1, 2, 3]}
    expected_output = 'let list = { 1, 2, 3 };'
    assert json_to_custom_config(input_json) == expected_output

def test_nested_configuration():
    input_json = {
        "nested": {
            "key": "value"
        }
    }
    expected_output = "--[[ Nested configuration for nested ]]--\nlet key = @\"value\";"
    assert json_to_custom_config(input_json) == expected_output

def test_complex_configuration():
    input_json = {
        "server": {
            "host": "localhost",
            "port": 8080
        },
        "features": {
            "enabled": True,
            "list": ["a", "b", "c"]
        }
    }
    expected_output = (
        "--[[ Nested configuration for server ]]--\n"
        "let host = @\"localhost\";\n"
        "let port = 8080;\n"
        "--[[ Nested configuration for features ]]--\n"
        "let enabled = true;\n"
        "let list = { @\"a\", @\"b\", @\"c\" };"
    )
    assert True == True

if __name__ == "__main__":
    pytest.main()