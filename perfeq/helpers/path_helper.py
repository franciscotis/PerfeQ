import os
from concurrent.futures import ThreadPoolExecutor, as_completed

class PathHelper:
    def __init__(self, path):
        """
        Inicializa a classe PathHelper com o caminho fornecido.

        Args:
            path (str): Caminho para um arquivo ou diretório.
        """
        self.path = path
        self.dir_path = ""

    def is_dir(self):
        """
        Verifica se o caminho é um diretório.

        Returns:
            bool: True se for um diretório, False caso contrário.
        """
        return os.path.isdir(self.path)

    def _read_file(self, file_path, language):
        """
        Lê o conteúdo de um arquivo.

        Args:
            file_path (str): Caminho do arquivo.
            language (str): Linguagem do arquivo (.py ou .c).

        Returns:
            dict: Dicionário contendo o conteúdo do arquivo, linguagem e caminho.
        """
        try:
            with open(file_path, encoding="utf8", errors="replace") as file:
                return {'language': language, 'file': file.read(), 'path': file_path}
        except FileNotFoundError:
            print(f"File '{file_path}' was not found. Skipping.")
        except PermissionError:
            print(f"Permission denied to read the file '{file_path}'. Skipping.")
        except Exception as e:
            print(f"An unexpected error occurred while reading '{file_path}': {e}")
        return None

    def _get_language(self, file_name):
        """
        Determina a linguagem com base na extensão do arquivo.

        Args:
            file_name (str): Nome do arquivo.

        Returns:
            str: Linguagem do arquivo ('.py' ou '.c'), ou None se não for suportado.
        """
        if file_name.endswith('.py'):
            return '.py'
        elif file_name.endswith('.c'):
            return '.c'
        return None

    def _process_directory(self, parallel=False):
        """
        Processa todos os arquivos no diretório especificado.

        Args:
            parallel (bool): Se True, lê arquivos em paralelo.

        Returns:
            list: Lista de dicionários com informações dos arquivos lidos.
        """
        files = []
        try:
            with os.scandir(self.path) as entries:
                # Filtra arquivos com extensões suportadas
                valid_entries = [
                    entry for entry in entries if entry.is_file() and self._get_language(entry.name)
                ]
                total_files = len(valid_entries)
                print(f"Total de arquivos a serem lidos: {total_files}")

                if parallel:
                    with ThreadPoolExecutor() as executor:
                        # Mapeia tarefas para leitura paralela
                        future_to_entry = {
                            executor.submit(self._read_file, entry.path, self._get_language(entry.name)): entry
                            for entry in valid_entries
                        }
                        for i, future in enumerate(as_completed(future_to_entry), start=1):
                            result = future.result()
                            if result:
                                files.append(result)
                            print(f"Arquivos restantes: {total_files - i}")
                else:
                    # Processa sequencialmente
                    for i, entry in enumerate(valid_entries, start=1):
                        language = self._get_language(entry.name)
                        result = self._read_file(entry.path, language)
                        if result:
                            files.append(result)
                        print(f"Arquivos restantes: {total_files - i}")
        except FileNotFoundError:
            raise FileNotFoundError(f"The directory '{self.path}' does not exist.")
        except PermissionError:
            raise PermissionError(f"Permission denied to access the directory '{self.path}'.")
        except Exception as e:
            print(f"An unexpected error occurred while processing '{self.path}': {e}")
        return files

    def _process_file(self):
        """
        Processa um único arquivo.

        Returns:
            list: Lista contendo o dicionário com informações do arquivo lido.
        """
        files = []
        try:
            language = self._get_language(self.path)
            if language:
                result = self._read_file(self.path, language)
                if result:
                    files.append(result)
        except Exception as e:
            print(f"An error occurred while accessing file '{self.path}': {e}")
        return files

    def get_content(self, parallel=False):
        """
        Obtém o conteúdo de arquivos no caminho especificado.

        Args:
            parallel (bool): Se True, lê arquivos em paralelo.

        Returns:
            list: Lista de dicionários com informações dos arquivos lidos.
        """
        if self.is_dir():
            self.dir_path = self.path
            return self._process_directory(parallel=parallel)
        else:
            self.dir_path = os.path.dirname(self.path)
            return self._process_file()
