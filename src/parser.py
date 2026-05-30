from dataclasses import dataclass, field
from datetime import datetime
from typing import Optional, List
from pathlib import Path
from email_main import Letter

class LetterExtractor:
    def extract(self, file_path):
        text = self.read_letter(file_path)
        headers, body = self.split_letter(text)

        return Letter(
            from_email = self.find_header(headers, "from", "от", "отправитель"),
            to=self.find_header(headers, "to", "кому", "получатель"),
            subject=self.find_header(headers, "subject", "тема"),
            date=self.parsing(self.find_header(headers, "date", "дата")),
            text=body,
            files=self.find_header(headers, "файл", "прикрепил"))

    def read_letter(self, path: str):
        with open(path, encoding="utf-8", errors="replace") as f:
            return f.read()

    def split_letter(self, text):
        headers_part, _, body = text.partition("\n\n")
        headers = {}
        for line in headers_part.splitlines():
            if ":" in line:
                name, _, value = line.partition(":")
                headers[name.strip().lower()] = value.strip()
        return headers, body

    def find_header(self, headers: dict, *aliases):
        for alias in aliases:
            if alias in headers:
                return headers[alias]
        return ""

    def parsing(self, date):
        if not date:
            return None
        for fmt in ("%Y-%m-%d %H:%M:%S", "%Y-%m-%d %H:%M", "%d.%m.%Y %H:%M:%S"):
            try:  
                return datetime.strptime(date, fmt)
            except ValueError:
                continue
        return None
