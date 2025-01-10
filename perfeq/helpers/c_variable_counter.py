import re

def c_variable_counter(code):
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