import os
import subprocess

from perfeq.constants import C_COMANDS, PYTHON_COMANDS
from perfeq.helpers.analyzers_helper import AnalyzersHelper
from perfeq.helpers.c_variable_counter import c_variable_counter
from perfeq.helpers.path_helper import PathHelper
from perfeq.helpers.python_variable_counter import python_variable_counter
from perfeq.models.code import Code
from perfeq.utils.enums import Languages


class Perfeq:
    def __init__(self, path):
        self.path_helper = PathHelper(path)
        self.codes = self.path_helper.get_content()
        self.current_code = None
        self.current_path = None
        self.current_language = None
        self.code_outputs = {}
        self.counter = {}
        self.warnings = {}
        self.result = []
        
        
    def analyze(self):
        """
        Analyzes the provided code files and collects the metrics and warnings.

        This method iterates through the list of code files, determines the language of each file,
        and counts the number of variables and functions in the file. It then runs additional
        analyzers on the code and collects the outputs. Finally, it decodes the analyzer warnings,
        stores the results, and prints them.

        Attributes:
            codes (list): A list of dictionaries containing 'file', 'path', and 'language' keys.
            current_code (str): The current code being analyzed.
            current_path (str): The path of the current code file.
            current_language (Languages): The programming language of the current code file.
            counter (dict): A dictionary storing the variable and function counts for each file path.
            code_outputs (dict): A dictionary storing the outputs of the analyzers for each file path.
            warnings (list): A list of decoded warnings from the analyzers.

        Methods:
            python_variable_counter(code: str) -> Tuple[int, int]: Counts variables and functions in Python code.
            c_variable_counter(code_lines: List[str]) -> Tuple[int, int]: Counts variables and functions in C code.
            run_analyzers() -> Any: Runs additional analyzers on the current code.
            store_result(warning_quantity_infos: Any) -> None: Stores the results of the analysis.
            print_result() -> None: Prints the results of the analysis.
        """
        for code in self.codes:
            self.current_code = code['file']
            self.current_path = code['path']
            if code['language'] == '.py':
                self.current_language = Languages.PYTHON
                variable_count, function_count = python_variable_counter(self.current_code)
                self.counter[self.current_path] = (variable_count, function_count)
            if code['language'] == '.c':
                self.current_language = Languages.C
                variable_count, function_count = c_variable_counter(self.current_code.splitlines())
                self.counter[self.current_path] = (variable_count, function_count)
            outputs = self.run_analyzers()
            self.code_outputs[code['path']] = outputs
        analyzers_helper = AnalyzersHelper(self.code_outputs)
        self.warnings = analyzers_helper.decode_analyzers()
        warning_quantity_infos = analyzers_helper.quantity_info
        self.store_result(warning_quantity_infos)
        self.print_result()
        
    def store_result(self, warning_quantity_infos):
        """
        Stores the analysis result for each code file.

        Args:
            warning_quantity_infos (dict): A dictionary where the keys are file paths and the values are objects containing
                                           the quantities of different types of warnings (variables, functions, formatting).

        Attributes:
            self.codes (list): A list of dictionaries, each containing 'file' and 'path' keys representing the code file and its path.
            self.counter (dict): A dictionary where the keys are file paths and the values are tuples containing the count of variables and functions.
            self.warnings (dict): A dictionary where the keys are file paths and the values are lists of warnings.
            self.result (list): A list to store the result objects for each code file.

        Result:
            Appends a Code object to self.result for each code file, containing the file path, warnings, line count, variable count,
            function count, and quantities of different types of warnings.
        """
        for code in self.codes:
            self.current_code = code['file']
            self.current_path = code['path']
            variable_count, function_count  = self.counter[self.current_path]
            warning_quantity_info = warning_quantity_infos[self.current_path]
            result = Code(self.current_path, self.warnings[self.current_path], len(self.current_code.splitlines()), 
                          variable_count, function_count, warning_quantity_info.warnings_variables_qty,
                          warning_quantity_info.warnings_functions_qty, warning_quantity_info.warnings_formatting_qty)
            self.result.append(result)
            

    def print_result(self):
        """
        Prints the result based on the number of codes.

        If there is only one code, it prints the result on the screen.
        Otherwise, it prints the results on a file.
        """
        if len(self.codes) == 1:
            self.print_single_result()
            return
        self.print_multiple_result()
        
    def print_single_result(self):
        """
        Prints the result of the first element in the result list.

        This method assumes that the first element in the `result` list has a 
        `print_result` method, which it calls to print the result.
        """
        code = self.result[0]
        code.print_result()
    
    def print_multiple_result(self):
        """
        Generates a CSV file containing the analysis results for multiple code segments.

        This method creates a directory named 'results' (if it doesn't already exist) 
        within the directory specified by `self.path_helper.dir_path`. It then writes 
        the analysis results to a file named 'perfeq_output.csv' in the 'results' directory.

        The CSV file contains the following columns:
        - code_id: Identifier for the code segment
        - LOC: Lines of Code
        - warnings_qty: Quantity of warnings
        - WPL: Warnings per Line
        - variable_warnings_qty: Quantity of variable-related warnings
        - variables_qty: Quantity of variables
        - VWPV: Variable Warnings per Variable
        - function_warnings_qty: Quantity of function-related warnings
        - functions_qty: Quantity of functions
        - FWPF: Function Warnings per Function
        - formatting_warnings_qty: Quantity of formatting-related warnings
        - FWPL: Formatting Warnings per Line

        Each row in the CSV file corresponds to the analysis results of a single code segment.

        Raises:
            OSError: If there is an issue creating the directory or writing to the file.
        """
        path = self.path_helper.dir_path + "/results"
        os.makedirs(path, exist_ok=True)
        with open(path +"/perfeq_output.csv", "w") as file:
            file.write("code_id,LOC,warnings_qty,WPL,variable_warnings_qty,variables_qty,VWPV,function_warnings_qty,functions_qty,FWPF,formatting_warnings_qty,FWPL\n")
            for code in self.result:
                file.write(code.print_multiple_result())
                file.write("\n")

            
                
    def run_analyzers(self):
        """
        Executes a set of analyzer commands based on the current programming language.
        This method determines the appropriate set of commands to run based on the 
        `current_language` attribute. It then executes each command, collects the 
        output, and returns a list of outputs.
        Returns:
            list: A list of outputs from the executed commands. If the command 
            execution is successful or the current language is Python, the standard 
            output is collected. Otherwise, the standard error is collected.
        """
        commands = PYTHON_COMANDS if self.current_language == Languages.PYTHON else C_COMANDS if self.current_language == Languages.C else ""
        if commands == "": 
            return
        outputs = []
        
        for command in commands:
            command+=self.current_path
            result = self.run_process(command)
            if result.returncode == 0 or self.current_language == Languages.PYTHON:
                output = result.stdout
                outputs.append(output)
            else:
                output = result.stderr
                outputs.append(output)
        return outputs
                
                                  
             
             
    def run_process(self, command):
        """
        Executes a given command in the shell and clears the terminal screen before running the command.

        Parameters:
        command (str): The command to be executed in the shell.

        Returns:
        subprocess.CompletedProcess: The result of the executed command, containing information such as 
                                     the return code, stdout, and stderr.
        """
        subprocess.run('cls' if os.name=='nt' else 'clear', shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, universal_newlines=True)
        return subprocess.run(command, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, universal_newlines=True)
        
