# чтение писем из архива Лена Коровина
import zipfile
import os
from typing import List, Optional, Union


class Reader:
    def __init__(self, zip="inbox.zip"):
        self.zip = zip
    
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
    


    def read_file(self, filename: str, is_text: bool = True) -> Optional[Union[str, bytes]]:

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
        if not self.if_valid():
            return []
        with zipfile.ZipFile(self.zip, 'r') as zf:
            return [name for name in zf.namelist()]
        


