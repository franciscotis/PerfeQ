import os

class PathHelper:
    def __init__(self, path):
        self.path = path
        self.dir_path = ""
        
    def is_dir(self):
        """
        Check if the given path is a directory.

        Returns:
            bool: True if the path is a directory, False otherwise.
        """
        return os.path.isdir(self.path)
    
    
    def get_content(self):
        """
        Retrieves the content of files in the specified directory or a single file.
        If the path is a directory, it lists all files in the directory and reads the content
        of files with extensions '.py' or '.c'. If the path is a file, it reads the content
        of the file if it has an extension '.py' or '.c'.
        Returns:
            list: A list of dictionaries, each containing:
                - 'language': The programming language of the file ('.py' or '.c').
                - 'file': The content of the file.
                - 'path': The path to the file.
        Raises:
            FileNotFoundError: If the directory or file does not exist.
            PermissionError: If there is no permission to access the directory or file.
            Exception: For any other unexpected errors.
        Prints:
            Error messages for files that cannot be read due to being not found, permission issues,
            or other unexpected errors.
        """
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