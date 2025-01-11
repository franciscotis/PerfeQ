import ast


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
    tree = ast.parse(code)
    variable_count = 0
    function_count = 0

    for node in ast.walk(tree):
        if isinstance(node, ast.Assign):
            variable_count += len(node.targets)
        elif isinstance(node, ast.FunctionDef):
            function_count += 1

    return variable_count, function_count
        
    