import re

def c_variable_counter(code):
    """
    Counts the number of variable declarations and function definitions in a given C code.
    Args:
        code (str): A string containing the C code to be analyzed.
    Returns:
        tuple: A tuple containing two integers:
            - variable_count (int): The number of variable declarations.
            - function_count (int): The number of function definitions.
    """
    function_pattern = re.compile(
    r'^[\w\s\*]+[\w\*]+\s*\([\w\s,]*\)\s*[{;]?$',
    re.MULTILINE
)
    variable_pattern = re.compile(r"\b(?!struct\b)([a-zA-Z_]\w*)\b\s+([a-zA-Z_]\w*(?:\s*,\s*[a-zA-Z_]\w*)*)\s*(;|=)")

    struct_pattern = re.compile(
        r'^\s*(typedef\s+)?struct(\s+\w+)?(\s*(\{[^}]*\})?)?\s*?', re.MULTILINE | re.DOTALL
    )
    
    function_count = 0
    variable_count = 0
    for line in code:
        line = line.strip()
        
        if function_pattern.match(line):
            function_count += 1
        elif variable_pattern.match(line):
            match = variable_pattern.match(line) 
            declaracoes = match.group(2) 
            variable_count += len([var.strip() for var in declaracoes.split(',') if var.strip()])
        elif struct_pattern.match(line):
            variable_count += 1
    

    return variable_count, function_count