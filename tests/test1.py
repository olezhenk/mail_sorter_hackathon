#PYTHONPATH=./src python3 tests/test1.py
import sys
import os
from parser import LetterExtractor

path = "/workspaces/mail_sorter_hackathon/tests/test_letter1"
extractor = LetterExtractor()
if not os.path.exists(path):
    print("Нет файла")
try:
    letter = extractor.extract(path)
    print(f"Отправитель:",letter.from_email)
    print(f"Получатель:", letter.to)
    print(f"Тема: ", letter.subject)
    print(f"Дата: ", letter.date)
    print(f"Текст: ", letter.text)
except Exception as e:
    print(f"Ошибка {e}")