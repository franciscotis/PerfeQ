import ast
import re

def python_variable_counter(code):
    """
    Counts the number of variable assignments and function definitions in a given Python code string.
    Args:
        code (str): A string containing Python code.
    Returns:
        tuple: A tuple containing two integers:
            - The first integer is the count of variable assignments.
            - The second integer is the count of function definitions.
    """
    try:
        tree = ast.parse(code)
        variable_count = 0
        function_count = 0

        for node in ast.walk(tree):
            if isinstance(node, ast.Assign):
                variable_count += len(node.targets)
            elif isinstance(node, ast.FunctionDef):
                function_count += 1

        return variable_count, function_count
    except:
        try:
            variable_count = count_variables_regex(code)
            function_count = count_function_regex(code)
            return variable_count, function_count
        except:
            return -1, -1

def count_function_regex(code):
    function_pattern = r'def\s+([a-zA-Z_]\w*)\s*\([^)]*\)\s*:'
    matches = re.findall(function_pattern, code)

    return len(matches)


def count_variables_regex(code):
    variable_pattern = r'\b(\w+)\s*=\s*(?!=)'

    matches = re.findall(variable_pattern, code)

    return len(matches)