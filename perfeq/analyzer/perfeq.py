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
        if len(self.codes) == 1:
            self.print_single_result()
            return
        self.print_multiple_result()
        
    def print_single_result(self):
        code = self.result[0]
        code.print_result()
    
    def print_multiple_result(self):
        path = self.path_helper.dir_path + "/results"
        os.makedirs(path, exist_ok=True)
        with open(path +"/perfeq_output.csv", "w") as file:
            file.write("code_id,LOC,warnings_qty,WPL,variable_warnings_qty,variables_qty,VWPV,function_warnings_qty,functions_qty,FWPF,formatting_warnings_qty,FWPL\n")
            for code in self.result:
                file.write(code.print_multiple_result())
                file.write("\n")

            
                
    def run_analyzers(self):
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
        subprocess.run('cls' if os.name=='nt' else 'clear', shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, universal_newlines=True)
        return subprocess.run(command, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, universal_newlines=True)
        
