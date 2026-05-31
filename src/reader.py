# чтение писем из архива Лена Коровина
import shutil
import tempfile
import zipfile
import os
from typing import List, Optional, Union


class Reader():
    def __init__(self, zip="inbox.zip", extractor=None):
        self.zip = zip
        self.extractor = extractor
        self.temporary_folder = None #все таки нужна временная папка для поэтапного добавления шагов как мы дошли до файла


    def creating_temporary_folder(self):
        if self.temporary_folder is None:
            self.temporary_folder = tempfile.mkdtemp() #создадим временную папку(директорию) для хранения адеса
        return self.temporary_folder
    


    def extract_to_temporary(self, filename: str):
        if not self.is_valid():
            return None
        if filename not in self.list_files():
            return None
        

        temporary_dir = self.creating_temporary_folder()
        abs_path = os.path.join(temporary_dir, os.path.basename(filename)) #просто встренные функции по нахождения адреса файла, но сдля этого необходима временная папка
        
        try:
            with zipfile.ZipFile(self.zip, 'r') as zf:
                data = zf.read(filename)
                with open(abs_path, 'wb') as f:
                        f.write(data)
            return os.path.abspath(abs_path)
        except Exception:
            return None


    def is_valid(self) -> bool:
        if not os.path.exists(self.zip):
            return False
        try:
            with zipfile.ZipFile(self.zip, 'r') as zf:
                if zf.testzip(): #тоже встренная функция в zipfile которая чекает сломан файл или не
                    return False
            return True
        
        except zipfile.BadZipFile:
            return False

    def read_file(self, filename: str, is_text: bool = True) -> Optional[Union[str, bytes, object]]:

        #для чтения txt через extract
        extension = self.get_file_extension(filename)
        if extension=='txt' and self.extractor is not None:
            abs_path = self.extract_to_temporary(filename)
            if abs_path:
                return self.extractor.extract(abs_path)
            else:
                return None


        if not self.is_valid():
            return None
        try:
            with zipfile.ZipFile(self.zip, 'r') as zf:
                data = zf.read(filename)
                if is_text:

                    try:
                        return data.decode('utf-8')
                    except UnicodeDecodeError:
                        return data.decode('cp1251', errors='replace')
                return data #потому что и так будет читаться в битовом представлении
        except KeyError:
            return None
        except Exception:
            return None


    def read_text(self, filename: str): #для чтения файлов txt, json
        return self.read_file(filename, is_text = True)

    def read_binary(self, filename: str): #для чтения jpeg, pdf, bin
        return self.read_file(filename, is_text = False)


    def get_file_extension(self, filename: str) ->  str:
        name, extension = os.path.splitext(filename)

        return extension.lower().lstrip('.') #удаляем точку из расширения, типо .txtx становится txt
    
    def get_file_size(self, filename: str):

        if not self.is_valid():
            return None

        try:
            with zipfile.ZipFile(self.zip, 'r') as zf:
                info = zf.getinfo(filename) #getinfo модуль из zipfile
                return info.file_size

        except KeyError:
            return None
        except Exception:
            return None


    def list_files(self): #не знаю надо или нет, но это выводит все файлы в зипе
        if not self.is_valid():
            return []
        with zipfile.ZipFile(self.zip, 'r') as zf:
            return [name for name in zf.namelist()]
    

    def cleanup(self): #отчистили всё
        if self.temporary_folder and os.path.exists(self.temporary_folder):
            shutil.rmtree(self.temporary_folder)
            self.temporary_folder = None 