#PYTHONPATH=./src python3 tests/test1.py
import sys
import os
from parser import LetterExtractor

test_letters = ["test_letter1", "test_letter2", "test_letter3", "test_letter4", "test_letter5"]
path = "/workspaces/mail_sorter_hackathon/tests/"
extractor = LetterExtractor()

for letter in test_letters:
    print(f"Письмо № {test_letters.index(letter) + 1}")
    full_path = os.path.join(path, letter)
    if not os.path.exists(full_path):
        print(f"Нет файла: {letter}")
        continue
    try:
        letter_obj = extractor.extract(full_path)
        print(f"Письмо: {letter}")
        print(f"Отправитель:", letter_obj.from_email)
        print(f"Получатель:", letter_obj.to)
        print(f"Тема: ", letter_obj.subject)
        print(f"Дата: ", letter_obj.date)
        print(f"Текст: ", letter_obj.text)
    except Exception as e:
        print(f"Ошибка при обработке {letter}: {e}")
