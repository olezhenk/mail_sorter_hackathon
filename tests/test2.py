#тест для reader.py
#PYTHONPATH=./src python3 tests/test2.py
import os
import sys
from reader import Reader

def run_tests(zip_path):
    reader = Reader(zip_path)
    if not reader.is_valid():
        print("Архив не найден.")

    files = reader.list_files()
    if not files:
        print("В архиве нет файлов.")
    else:
        print(files)

    test_file = files[0]
    if test_file.lower().endswith(('.txt', '.json', '.log', '.md')):
        txt = reader.read_text(test_file)
        print(txt)

    raw = reader.read_binary(test_file)
    print(raw)

    size = reader.get_file_size(test_file)
    print(size)

if __name__ == "__main__":
    zip_path = "/workspaces/mail_sorter_hackathon/inbox.zip"
    
    if not os.path.exists(zip_path):
        print(f"Файл не найден: {zip_path}")
        sys.exit(1)
    success = run_tests(zip_path)
    sys.exit(0 if success else 1)