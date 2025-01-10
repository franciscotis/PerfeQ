import os

class PathHelper:
    def __init__(self, path):
        self.path = path
        self.dir_path = ""
        
    def is_dir(self):
        return os.path.isdir(self.path)
    
    
    def get_content(self):
        files = []
        try:
            if self.is_dir():
                self.dir_path = self.path
                try:
                    codes = os.listdir(self.path)
                except FileNotFoundError:
                    raise FileNotFoundError(f"The directory '{self.path}' does not exist.")
                except PermissionError:
                    raise PermissionError(f"Permission denied to access the directory '{self.path}'.")

                for code in codes:
                    language = ".py" if ".py" in code else ".c" if ".c" in code else None
                    if language is not None:
                        code_path = self.path + "/" + code
                        try:
                            with open(code_path, encoding="utf8") as file:
                                files.append({'language': language,'file': file.read(), 'path': code_path})
                        except FileNotFoundError:
                            print(f"File '{code_path}' was not found. Skipping.")
                        except PermissionError:
                            print(f"Permission denied to read the file '{code_path}'. Skipping.")
                        except Exception as e:
                            print(f"An unexpected error occurred while reading '{code_path}': {e}")   
            else:
                self.dir_path = os.path.dirname(self.path)
                language = ".py" if ".py" in self.path else ".c" if ".c" in self.path else None
                with open(self.path, encoding="utf8") as file:
                    files.append({'language': language,'file': file.read(), 'path': self.path})
        except Exception as e:
            print(f"An error occurred while accessing content in '{self.path}': {e}")
        return files