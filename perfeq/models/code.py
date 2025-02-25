class Code:
    def __init__(self, id, warnings, lines_of_code, variables_qty, functions_qty, variables_warnings_qty, functions_warnings_qty, formatting_warnings_qty):
        self.id = id
        self.warnings = warnings
        self.warnings.sort(key=lambda warning: warning.line)
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
        """
        Calculate various metrics related to warnings and code characteristics.

        This method calculates the following metrics:
        - warnings_per_lines_of_code: The ratio of the number of warnings to the total lines of code.
        - variable_warnings_per_number_of_variables: The ratio of the number of variable-related warnings to the total number of variables.
        - function_warnings_per_number_of_functions: The ratio of the number of function-related warnings to the total number of functions.
        - formatting_warnings_per_lines_of_code: The ratio of the number of formatting-related warnings to the total lines of code.

        These metrics are set as attributes of the instance.
        """
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
        """
        Prints the results of the analysis including warnings and various metrics.
        The output includes:
        - A list of warnings with their respective line numbers and messages.
        - Metrics such as:
            - Warnings per lines of code (WPL) as a percentage.
            - Variable Warnings per number of variables (VWPV) as a percentage.
            - Function Warnings per number of functions (FWPF) as a percentage.
            - Formatting warnings per lines of code (FWPL) as a percentage.
        """
        print("Warnings:\n")
        for warning in self.warnings:
            print(f"[{warning.line}] - {warning.message}")
        print("\n")
        print("Metrics:\n")
        print("QTD FUNÇÔES: ", self.functions_qty)
        print(f"Warnings per lines of code (WPL) - {self.warnings_per_lines_of_code*100:.2f}%\n")
        print(f"Variable Warnings per number of variables (VWPV) - {self.variable_warnings_per_number_of_variables*100:.2f}%\n")
        print(f"Function Warnings per number of functions (FWPF) - {self.function_warnings_per_number_of_functions*100:.2f}%\n")
        print(f"Formatting warnings per lines of code (FWPL) - {self.formatting_warnings_per_lines_of_code*100:.2f}%\n")
        
    
    def print_multiple_result(self):
        """
        Returns a formatted string with the results of the analysis.
        
        The output includes:
        - ID of the code.
        - Total lines of code.
        - Total number of warnings.
        - Warnings per lines of code (WPL) as a percentage.
        - Total number of variable-related warnings.
        - Total number of variables.
        - Variable Warnings per number of variables (VWPV) as a percentage.
        - Total number of function-related warnings.
        - Total number of functions.
        - Function Warnings per number of functions (FWPF) as a percentage.
        - Total number of formatting-related warnings.
        - Formatting warnings per lines of code (FWPL) as a percentage.
        """
        return (
            f"{self.id},{self.lines_of_code},{len(self.warnings)},"
            f"{self.warnings_per_lines_of_code*100:.2f},{self.variables_warnings_qty},"
            f"{self.variables_qty},{self.variable_warnings_per_number_of_variables*100:.2f},"
            f"{self.functions_warnings_qty},{self.functions_qty},"
            f"{self.function_warnings_per_number_of_functions*100:.2f},"
            f"{self.formatting_warnings_qty},{self.formatting_warnings_per_lines_of_code*100:.2f}"
        )