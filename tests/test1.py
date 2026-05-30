import sys
import os
from parser import LetterExtractor

path = "/workspaces/mail_sorter_hackathon/tests/test_letter1"
extractor = LetterExtractor()
if not os.path.exists(path):
    print("Нет файла")
try:
    letter = extractor.extract(path)
    print(f"Отправитель:",letter.sender)
    print(f"Получатель:", letter.recipient)
    print(f"Тема: ", letter.subject)
    print(f"Дата: ", letter.date)
    print(f"Текст: ", letter.text_body)
except Exception as e:
    print(f"Ошибка")