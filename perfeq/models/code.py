class Code:
    def __init__(self, id, warnings, lines_of_code, variables_qty, functions_qty, variables_warnings_qty, functions_warnings_qty, formatting_warnings_qty):
        self.id = id
        self.warnings = warnings
        self.lines_of_code = lines_of_code
        self.variables_qty = variables_qty
        self.functions_qty = functions_qty
        self.variables_warnings_qty = variables_warnings_qty
        self.functions_warnings_qty = functions_warnings_qty
        self.formatting_warnings_qty = formatting_warnings_qty
        
        self.warnings_per_lines_of_code = 0
        self.variable_warnings_per_number_of_variables = 0
        self.function_warnings_per_number_of_functions = 0
        self.formatting_warnings_per_lines_of_code = 0
        
        self.calculate_metrics()

            
    def calculate_metrics(self):
        self.warnings_per_lines_of_code = (
            len(self.warnings) / self.lines_of_code if self.lines_of_code != 0 else 0
        )
        self.variable_warnings_per_number_of_variables = (
            self.variables_warnings_qty / self.variables_qty if self.variables_qty != 0 else 0
        )
        self.function_warnings_per_number_of_functions = (
            self.functions_warnings_qty / self.functions_qty if self.functions_qty != 0 else 0
        )
        self.formatting_warnings_per_lines_of_code = (
            self.formatting_warnings_qty / self.lines_of_code if self.lines_of_code != 0 else 0
        )

    def print_result(self):
        print("Warnings:\n")
        for warning in self.warnings:
            print(f"[{warning.line}] - {warning.message}")
        print("\n")
        print("Metrics:\n")
        
        print(f"Warnings per lines of code (WPL) - {self.warnings_per_lines_of_code*100:.2f}%\n")
        print(f"Variable Warnings per number of variables (VWPV) - {self.variable_warnings_per_number_of_variables*100:.2f}%\n")
        print(f"Function Warnings per number of functions (FWPF) - {self.function_warnings_per_number_of_functions*100:.2f}%\n")
        print(f"Formatting warnings per lines of code (FWPL) - {self.formatting_warnings_per_lines_of_code*100:.2f}%\n")
        
    
    def print_multiple_result(self):
        return f"{self.id},{self.lines_of_code},{len(self.warnings)},{self.warnings_per_lines_of_code:.2f},{self.variables_warnings_qty},{self.variables_qty},{self.variable_warnings_per_number_of_variables:.2f},{self.functions_warnings_qty},{self.functions_qty},{self.function_warnings_per_number_of_functions:.2f},{self.formatting_warnings_qty},{self.formatting_warnings_per_lines_of_code:.2f}"