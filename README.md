  

# PerfeQ

An integrated source code quality assessment tool focusing on adherence to programming language style conventions
  

## Install

  
For command line use, you can install using the following command:

  

```bash

pip install perfeq

```

## How to use

  

You can start using the analyzer by providing the relative path of the code that you want to analyze:

```python

perfeq C:\Documents\Codes\my_code.c

```
Or if you want to analyze multiple codes, you can provide the relative path of the folder where the codes are located:
  
  ```python

perfeq C:\Documents\Codes

```

The tool analyzes codes written in C and Python with the following static analyzers:

### C Analyzers:

 - [Cpplint](https://github.com/cpplint/cpplint)
 - [NamingCheck](https://github.com/franciscotis/NamingCheck)

### Python Analyzers:
 - [Pylint](https://github.com/pylint-dev/pylint)
 - [NamingCheck](https://github.com/franciscotis/NamingCheck)
  
After using the command to start the tool, it'll run the static analyzers - which will provide the warning messages. These messages combining with some descriptions of the code (such as quantity of lines of code) were used to create metrics that can describe mathematically the analyzed code in therms of code quality.  The metrics are:
 - Number of warning messages (general) per LOC (WPL)
 - Number of warning messages related to variable declaration per number of variables (VWPV)
 - Number of warning messages related to function declaration per number of functions (FWPF)
 - Number of warning messages related to code formatting per LOC (FWPL)

The values of the metrics can help developers to understand the level of quality of their code.


### Analyzing a single file

When analyzing a single file, it will display on the terminal all the warning messages provided by the static analyzer, following the calculated metrics values.


![PerfeQ Output](./resources/perfeq-output.png "PerfeQ Output")


### Analyzing multiples files

  When analyzing multiples files, it won't display on the terminal all the warning messages. Although it'll create a .csv file on the path of the analyzed codes. This file contains some description of the code and the values of the metrics:
 
    code_id,LOC,warnings_qty,WPL,variable_warnings_qty,variables_qty,VWPV,function_warnings_qty,functions_qty,FWPF,formatting_warnings_qty,FWPL


![PerfeQ Output](./resources/perfeq-csv-file.png "PerfeQ Output")