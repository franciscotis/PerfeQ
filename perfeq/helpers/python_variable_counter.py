import ast
import re


def python_variable_counter(code):
    tree = ast.parse(code)
    variable_count = 0
    function_count = 0

    for node in ast.walk(tree):
        if isinstance(node, ast.Assign):
            variable_count += len(node.targets)
        elif isinstance(node, ast.FunctionDef):
            function_count += 1

    return variable_count, function_count
        
    