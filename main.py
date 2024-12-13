import argparse
import json
import re

def json_to_custom_config(json_obj):
    """Converts JSON object to custom configuration language format."""
    def format_value(value):
        if isinstance(value, str):
            return f'@"{value}"'
        elif isinstance(value, (int, float)):
            return str(value)
        elif isinstance(value, list):
            return "{ " + ", ".join(format_value(v) for v in value) + " }"
        else:
            raise ValueError(f"Unsupported value type: {type(value)}")

    def process_key_value(key, value):
        return f"let {key} = {format_value(value)};"

    result = []
    for key, value in json_obj.items():
        if isinstance(value, dict):
            result.append(f"--[[ Nested configuration for {key} ]]--")
            nested = json_to_custom_config(value)
            result.append(nested)
        else:
            result.append(process_key_value(key, value))
    return "\n".join(result)

def parse_json_file(input_file):
    """Parses JSON from the input file."""
    try:
        with open(input_file, 'r', encoding='utf-8') as f:
            return json.load(f)
    except json.JSONDecodeError as e:
        raise ValueError(f"Error parsing JSON file: {e}")

def write_output_file(output_file, content):
    """Writes the transformed content to the output file."""
    with open(output_file, 'w', encoding='utf-8') as f:
        f.write(content)

def main():
    parser = argparse.ArgumentParser(description="Transform JSON into a custom configuration language.")
    parser.add_argument("-i", "--input", required=True, help="Path to the input JSON file.")
    parser.add_argument("-o", "--output", required=True, help="Path to the output configuration file.")

    args = parser.parse_args()

    try:
        json_data = parse_json_file(args.input)
        config_data = json_to_custom_config(json_data)
        write_output_file(args.output, config_data)
        print("Transformation successful. Output written to:", args.output)
    except Exception as e:
        print("Error:", e)

if __name__ == "__main__":
    main()
