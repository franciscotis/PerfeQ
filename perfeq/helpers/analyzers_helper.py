from perfeq.constants import DIVIDER_1_PYLINT, DIVIDER_2_PYLINT, DIVIDER_3_PYLINT
from perfeq.models.quantity_info import QuantityInfo
from perfeq.models.warning_message import WarningMessage
from perfeq.utils.enums import TypesOfWarning


class AnalyzersHelper:
    def __init__(self, warnings):
        self.warnings = warnings
        self.warnings_decoded = {}
        self.quantity_info = {}
        
    def decode_analyzers(self):
        outputs = {}
        for key,value in self.warnings.items():
            if(len(value) > 0):
                for output in value:
                    for line in output.splitlines():
                        if(line != '' and not DIVIDER_1_PYLINT in line and not DIVIDER_2_PYLINT in line and not DIVIDER_3_PYLINT in line):
                            saida =  key + ";" + line
                            if key not in outputs:
                                outputs[key] = []
                            outputs[key].append(saida)
        outputs = self.decode_naming_check(outputs)
        outputs = self.decode_cpplint(outputs)
        outputs = self.decode_pylint(outputs)
            
        return self.warnings_decoded
    
    def update_quantity_info(self, key, type_of_warning):
        if key not in self.quantity_info:
            self.quantity_info[key] = QuantityInfo()
        if type_of_warning == TypesOfWarning.FUNCTION:
            self.quantity_info[key].warnings_functions_qty+=1
        elif type_of_warning ==  TypesOfWarning.VARIABLE:
            self.quantity_info[key].warnings_variables_qty+=1
        else:
            self.quantity_info[key].warnings_formatting_qty+=1
        
    def decode_naming_check(self, outputs):
        non_decoded = {}
        for key,value in outputs.items():
            for output in value:
                if "WARN" in output:
                    output = output.split("WARN:")
                    message_line = output[1].split("]")
                    line = message_line[0].replace("[", "").strip()
                    message = message_line[1].strip()
                    type_of_warning = TypesOfWarning.FUNCTION if "Functions" in message else TypesOfWarning.VARIABLE
                    warning_message = WarningMessage(message, line, type_of_warning)
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
        non_decoded = {}
        for key,value in outputs.items():
            for output in value:
                if ".c" in output:
                    output = output.split(";",1)[1].split(":",1)
                    message_line = output[1].split(":",1)
                    line = message_line[0]
                    message = message_line[1].strip()
                    warning_message = WarningMessage(message, line, TypesOfWarning.FORMATTING)
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
        warning_keywords = {
            "Function": TypesOfWarning.FUNCTION,
            "Constant": TypesOfWarning.VARIABLE,
            "Variable": TypesOfWarning.VARIABLE,
        }
        non_decoded = {}
        for key,value in outputs.items():
            for output in value:
                if ".py" in output:
                    output = output.split(";",1)[1].split(":",1)
                    message_line = output[1].split(":",1)
                    line = message_line[0]
                    message = message_line[1].split(":",1)[1].split(":")[1].strip()
                    type_of_warning = next((warning_type for keyword, warning_type in warning_keywords.items() if keyword in message),TypesOfWarning.FORMATTING)
                    self.update_quantity_info(key, type_of_warning)
                    warning_message = WarningMessage(message, line, type_of_warning)
                    if key not in self.warnings_decoded:
                        self.warnings_decoded[key] = []
                    self.warnings_decoded[key].append(warning_message)
                else:
                    non_decoded[key].append(output)
        return non_decoded
                