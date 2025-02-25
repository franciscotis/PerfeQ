import concurrent
from perfeq.constants import DIVIDER_1_PYLINT, DIVIDER_2_PYLINT, DIVIDER_3_PYLINT
from perfeq.models.quantity_info import QuantityInfo
from perfeq.models.warning_message import WarningMessage
from perfeq.utils.enums import TypesOfWarning
from concurrent.futures import ThreadPoolExecutor
from tqdm import tqdm


class AnalyzersHelper:
    def __init__(self, warnings):
        self.warnings = warnings
        self.warnings_decoded = {}
        self.quantity_info = {}
        
    def decode_analyzers(self):
        """
        Decodes analyzer warnings and processes them into a structured format in parallel.
        This method iterates through the warnings stored in `self.warnings`, processes
        each warning output in parallel, and filters out lines that contain specific dividers.
        The processed warnings are then passed through additional decoding functions
        for naming checks, cpplint, and pylint.

        Returns:
            dict: A dictionary containing the decoded warnings, structured by their
            respective analyzer keys.
        """
        def process_warning(key, value):
            processed = []
            for output in value:
                for line in output.splitlines():
                    if (line != '' and
                            not DIVIDER_1_PYLINT in line and
                            not DIVIDER_2_PYLINT in line and
                            not DIVIDER_3_PYLINT in line):
                        processed.append(key + ";" + line)
            return key, processed

        outputs = {}

        # Parallel processing of warnings with progress tracking
        with ThreadPoolExecutor() as executor:
            futures = {executor.submit(process_warning, key, value): key for key, value in self.warnings.items()}

            for future in tqdm(concurrent.futures.as_completed(futures), total=len(futures), desc="Decoding warnings"):
                key, processed = future.result()
                if key not in outputs:
                    outputs[key] = []
                outputs[key].extend(processed)

        # Further decoding steps
        outputs = self.decode_naming_check(outputs)
        outputs = self.decode_cpplint(outputs)
        outputs = self.decode_pylint(outputs)

        return self.warnings_decoded

    
    def update_quantity_info(self, key, type_of_warning):
        """
        Updates the quantity information for a given key based on the type of warning.

        Args:
            key (str): The key for which the quantity information is to be updated.
            type_of_warning (TypesOfWarning): The type of warning to update the quantity for.
                It can be one of the following:
                - TypesOfWarning.FUNCTION: Increments the function warnings quantity.
                - TypesOfWarning.VARIABLE: Increments the variable warnings quantity.
                - TypesOfWarning.FORMATTING: Increments the formatting warnings quantity.

        Returns:
            None
        """
        if key not in self.quantity_info:
            self.quantity_info[key] = QuantityInfo()
        if type_of_warning == TypesOfWarning.FUNCTION:
            self.quantity_info[key].warnings_functions_qty+=1
        elif type_of_warning ==  TypesOfWarning.VARIABLE:
            self.quantity_info[key].warnings_variables_qty+=1
        else:
            self.quantity_info[key].warnings_formatting_qty+=1
        
    def decode_naming_check(self, outputs):
        """
        Decodes warning messages from the given outputs and categorizes them.

        Args:
            outputs (dict): A dictionary where keys are identifiers and values are lists of output strings.

        Returns:
            dict: A dictionary containing non-decoded outputs categorized by their keys.

        The function processes each output string in the provided dictionary. If an output string contains a warning 
        (indicated by the presence of "WARN"), it extracts the warning message, line number, and type of warning 
        (either function or variable). It then updates the quantity information and stores the decoded warning message 
        in the `warnings_decoded` attribute. If an output string does not contain a warning, it is added to the 
        `non_decoded` dictionary, which is returned at the end.
        """
        non_decoded = {}
        for key,value in outputs.items():
            for output in value:
                if "WARN" in output:
                    output = output.split("WARN:")
                    message_line = output[1].split("]")
                    line = message_line[0].replace("[", "").strip()
                    message = message_line[1].strip()
                    type_of_warning = TypesOfWarning.FUNCTION if "Functions" in message else TypesOfWarning.VARIABLE
                    warning_message = WarningMessage(message, int(line), type_of_warning)
                    self.update_quantity_info(key, type_of_warning)
                    if key not in self.warnings_decoded:
                        self.warnings_decoded[key] = []
                    self.warnings_decoded[key].append(warning_message)
                else:
                    if key not in non_decoded:
                        non_decoded[key] = []
                    non_decoded[key].append(output)
        return non_decoded
    
    def decode_cpplint(self, outputs):
        """
        Decodes the output of cpplint and categorizes warnings.

        Args:
            outputs (dict): A dictionary where keys are file names and values are lists of cpplint output strings.

        Returns:
            dict: A dictionary containing non-decoded outputs categorized by file names.

        The function processes each output string associated with a file. If the output string
        pertains to a C file (indicated by ".c" in the string), it extracts the line number and
        warning message, creates a WarningMessage object, and updates the warnings_decoded
        dictionary and quantity information. If the output string does not pertain to a C file,
        it is added to the non_decoded dictionary.
        """
        non_decoded = {}
        for key,value in outputs.items():
            for output in value:
                if ".c" in output:
                    if "UnicodeDecodeError" in output:
                        continue
                    output = output.split(";",1)[1].split(":",1)
                    if len(output) < 2:
                        continue
                    message_line = output[1].split(":",1)[1].split(":")
                    if len(message_line) < 2:
                        continue
                    line = message_line[0]
                    message = message_line[1].strip()
                    warning_message = WarningMessage(message, int(line), TypesOfWarning.FORMATTING)
                    self.update_quantity_info(key, TypesOfWarning.FORMATTING)
                    if key not in self.warnings_decoded:
                        self.warnings_decoded[key] = []
                    self.warnings_decoded[key].append(warning_message)
                else:
                    if key not in non_decoded:
                        non_decoded[key] = []
                    non_decoded[key].append(output)
        return non_decoded
    
    def decode_pylint(self, outputs):
        """
        Decodes pylint output messages and categorizes them into warnings.

        Args:
            outputs (dict): A dictionary where keys are filenames and values are lists of pylint output strings.

        Returns:
            dict: A dictionary of non-decoded outputs, where keys are filenames and values are lists of non-decoded output strings.

        The function processes each pylint output string, extracts the line number and message, determines the type of warning based on predefined keywords, 
        and updates the quantity information for each type of warning. It then creates a WarningMessage object and appends it to the warnings_decoded dictionary.
        If the output string does not contain a ".py" file reference, it is added to the non_decoded dictionary.
        """
        warning_keywords = {
            "Function": TypesOfWarning.FUNCTION,
            "Constant": TypesOfWarning.VARIABLE,
            "Variable": TypesOfWarning.VARIABLE,
        }
        non_decoded = {}
        for key,value in outputs.items():
            for output in value:
                if ".py:" in output:
                    output = output.split(".py:")[1]
                    message_line = output.split(":",1)
                    line = message_line[0]
                    message = message_line[1].split(":",1)[1].split(":")[1].strip()
                    type_of_warning = next((warning_type for keyword, warning_type in warning_keywords.items() if keyword in message),TypesOfWarning.FORMATTING)
                    self.update_quantity_info(key, type_of_warning)
                    warning_message = WarningMessage(message, int(line), type_of_warning)
                    if key not in self.warnings_decoded:
                        self.warnings_decoded[key] = []
                    self.warnings_decoded[key].append(warning_message)
                else:
                    if key not in non_decoded:
                        non_decoded[key] = []
                    non_decoded[key].append(output)
        return non_decoded
                