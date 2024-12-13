import argparse
import json
import re

def evaluate_expression(expression, variables):
    if not expression.startswith("^"):
        raise ValueError("Invalid expression format. Must start with '^'.")
    tokens = re.findall(r'[^\s\(\)]+', expression[1:])
    if len(tokens) < 2:
        raise ValueError("Invalid expression format. Must contain operator and arguments.")
    operator = tokens[0]
    operands = tokens[1:]
    def get_value(token):
        if token in variables:
            return variables[token]
        try:
            return int(token)
        except ValueError:
            raise ValueError(f"Unknown variable or invalid operand: {token}")
    values = list(map(get_value, operands))
    if operator == "+":
        return sum(values)
    elif operator == "-":
        if len(values) != 2:
            raise ValueError("Subtraction requires exactly two operands.")
        return values[0] - values[1]
    elif operator == "print":
        print(*values)
        return None
    else:
        raise ValueError(f"Unsupported operator: {operator}")

def format_value(value, variables):
    if isinstance(value, str):
        if value.startswith("^"):
            return str(evaluate_expression(value, variables))
        return f'@"{value}"'
    elif isinstance(value, (int, float)):
        return str(value)
    elif isinstance(value, list):
        return "{ " + ", ".join(format_value(v, variables) for v in value) + " }"
    else:
        raise ValueError(f"Unsupported value type: {type(value)}")

def json_to_custom_config(json_obj, variables=None, indent=0):
    if variables is None:
        variables = {}

    def process_key_value(key, value, indent_level):
        indent_str = " " * indent_level
        if isinstance(value, str) and value.startswith("^"):
            computed_value = evaluate_expression(value, variables)
            variables[key] = computed_value
            return f"{indent_str}{key} = {computed_value};"
        elif isinstance(value, dict):
            return f"{indent_str}{key} = {{\n{{{json_to_custom_config(value, variables, indent_level + 4)}}}\n{indent_str}}};"
        elif isinstance(value, list):
            formatted_list = ", ".join(format_value(v, variables) for v in value)
            return f"{indent_str}{key} = {{ {formatted_list} }};"
        else:
            variables[key] = value
            return f"{indent_str}{key} = {format_value(value, variables)};"

    result = []
    indent_str = " " * indent
    for key, value in json_obj.items():
        result.append(process_key_value(key, value, indent))

    return "\n".join(result)


def parse_json_file(input_file):
    with open(input_file, 'r', encoding='utf-8') as f:
        return json.load(f)

def write_output_file(output_file, content):
    with open(output_file, 'w', encoding='utf-8') as f:
        f.write(content)

def wrap_in_braces(config_data):
    return f"{{\n{config_data}\n}}"

# Example usage in the script remains unchanged.
def main():
    parser = argparse.ArgumentParser(description="Transform JSON into a custom configuration language.")
    parser.add_argument("-i", "--input", required=True, help="Path to the input JSON file.")
    parser.add_argument("-o", "--output", required=True, help="Path to the output configuration file.")
    args = parser.parse_args()
    try:
        json_data = parse_json_file(args.input)
        config_data = json_to_custom_config(json_data)
        wrapped_config_data = wrap_in_braces(config_data)
        write_output_file(args.output, wrapped_config_data)
        print("Transformation successful. Output written to:", args.output)
    except Exception as e:
        print("Error:", e)

if __name__ == "__main__":
    main()
