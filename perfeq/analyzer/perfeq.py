import os
import subprocess
import pickle
from concurrent.futures import ThreadPoolExecutor, as_completed
from threading import Lock
from tqdm import tqdm

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
        self.codes = self.path_helper.get_content(True)
        self.current_code = None
        self.current_path = None
        self.current_language = None
        self.code_outputs = {}
        self.counter = {}
        self.warnings = {}
        self.result = []
        self.lock = Lock()  # Lock para sincronizar o acesso à contagem
        self.remaining_files = len(self.codes)  # Número total de arquivos a serem processados

    def analyze(self):
        """
        Analyzes the provided code files in parallel and collects the metrics and warnings.
        """
        print(f"Iniciando análise em paralelo ({self.remaining_files} arquivos no total)")

        # Primeiro, faz a contagem de variáveis e funções para cada arquivo
        for code in self.codes:
            self.current_code = code['file']
            self.current_path = code['path']
            if code['language'] == '.py':
                self.current_language = Languages.PYTHON
                variable_count, function_count = python_variable_counter(self.current_code)
            elif code['language'] == '.c':
                self.current_language = Languages.C
                variable_count, function_count = c_variable_counter(self.current_code.splitlines())
            else:
                continue

            self.counter[self.current_path] = (variable_count, function_count)

        # Executa os analisadores em paralelo
        outputs = self.run_analyzers_parallel()
        self.code_outputs.update(outputs)

        # Decodifica os avisos e armazena os resultados
        analyzers_helper = AnalyzersHelper(self.code_outputs)
            
        self.warnings = analyzers_helper.decode_analyzers()
        warning_quantity_infos = analyzers_helper.quantity_info
        self.store_result(warning_quantity_infos)
        self.print_result()

    def store_result(self, warning_quantity_infos):
        """
        Stores the analysis result for each code file.
        """
        for code in self.codes:
            self.current_code = code['file']
            self.current_path = code['path']
            variable_count, function_count = self.counter[self.current_path]
            warning_quantity_info = warning_quantity_infos[self.current_path]
            result = Code(
                self.current_path,
                self.warnings[self.current_path],
                len(self.current_code.splitlines()),
                variable_count,
                function_count,
                warning_quantity_info.warnings_variables_qty,
                warning_quantity_info.warnings_functions_qty,
                warning_quantity_info.warnings_formatting_qty,
            )
            self.result.append(result)

    def print_result(self):
        """
        Prints the result based on the number of codes.
        """
        if len(self.codes) == 1:
            self.print_single_result()
            return
        self.print_multiple_result()

    def print_single_result(self):
        """
        Prints the result of the first element in the result list.
        """
        code = self.result[0]
        code.print_result()

    def print_multiple_result(self):
        """
        Generates a CSV file containing the analysis results for multiple code segments.
        """
        path = os.path.join(self.path_helper.dir_path, "results")
        os.makedirs(path, exist_ok=True)
        with open(os.path.join(path, "perfeq_output.csv"), "w") as file:
            file.write(
                "code_id,LOC,warnings_qty,WPL,variable_warnings_qty,variables_qty,VWPV,function_warnings_qty,functions_qty,FWPF,formatting_warnings_qty,FWPL\n"
            )
            for code in self.result:
                file.write(code.print_multiple_result())
                file.write("\n")

    def run_analyzers_parallel(self):
        """
        Executes analyzers for all code files in parallel.

        Returns:
            dict: A dictionary mapping file paths to their analyzer outputs.
        """
        outputs = {}

        def process_file(code):
            """
            Runs analyzers for a single file and returns the results.

            Args:
                code (dict): Dictionary with 'file', 'path', and 'language' keys.

            Returns:
                tuple: The file path and its analyzer outputs.
            """
            self.current_code = code['file']
            self.current_path = code['path']
            self.current_language = (
                Languages.PYTHON if code['language'] == '.py' else Languages.C if code['language'] == '.c' else None
            )
            result = self.run_analyzers()

            # Atualiza o contador de arquivos restantes
            with self.lock:
                self.remaining_files -= 1
                print(f"{self.remaining_files} arquivos restantes...")

            return code['path'], result

        # Executa em paralelo usando ThreadPoolExecutor
        with ThreadPoolExecutor() as executor:
            future_to_code = {
                executor.submit(process_file, code): code for code in self.codes
            }
            for future in as_completed(future_to_code):
                file_path, output = future.result()
                outputs[file_path] = output
        return outputs

    def run_analyzers(self):
        """
        Executes a set of analyzer commands based on the current programming language
        and displays progress using a progress bar.
        """
        commands = (
            PYTHON_COMANDS
            if self.current_language == Languages.PYTHON
            else C_COMANDS
            if self.current_language == Languages.C
            else ""
        )
        if not commands:
            return []
        
        outputs = []

        # Barra de progresso usando tqdm
        with tqdm(total=len(commands), desc="Running Analyzers", unit="command") as pbar:
            for command in commands:
                command += self.current_path
                result = self.run_process(command)
                if result.returncode == 0 or self.current_language == Languages.PYTHON:
                    outputs.append(result.stdout)
                else:
                    outputs.append(result.stderr)
                # Atualiza a barra de progresso
                pbar.update(1)

        return outputs

    def run_process(self, command):
        """
        Executes a given command in the shell.

        Returns:
            subprocess.CompletedProcess: The result of the executed command.
        """
        return subprocess.run(command, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, universal_newlines=True)
