# test_run.py
import sys
import os
from parser import LetterExtractor

extractor = LetterExtractor()
if not os.path.exists("/workspaces/mail_sorter_hackathon/src/test_letter1"):
    print("Нет файла")
try:
    letter = extractor.extract("/workspaces/mail_sorter_hackathon/src/test_letter1")
    print(f"Отправитель:",letter.sender)
    print(f"Получатель:", letter.recipient)
    print(f"Тема: ", letter.subject)
    print(f"Дата: ", letter.date)
    print(f"Текст: ", letter.text_body)
except Exception as e:
    print(f"Ошибка")