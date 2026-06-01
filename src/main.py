from rules_classifier import *
from parser import LetterExtractor
from reader import Reader
from email_main import Letter
from actions import emailsort
import os

extractor = LetterExtractor()
reader = Reader(zip="inbox.zip", extractor=extractor)

# Правила для классификации
classifier = main_classifier(default_category="inbox", stop_on_first_match=True)
#от руководства
boss_rule = sender_rule(['@company.ru', 'ceo@company.ru', 'boss@company.ru'], False)
classifier.add_rule(boss_rule, "from_boss", 1)
#спам
spam_rule = keyword_rule(['акция', 'выигрыш', 'распродажа', 'лотерея', 'скидка'], False, "both")
classifier.add_rule(spam_rule, "spam", 100)
#срочное
urgent_rule = keyword_rule(['срочно', 'быстро', 'незамедлительно', 'до конца дня', 'критично'], False, "both")
classifier.add_rule(urgent_rule, "urgent", 5)
#финансовое
finance_rule = sender_rule(['sberbank.ru', 'alfa.ru', 'tbank.ru', 'vtb.ru'], False)
classifier.add_rule(finance_rule, "finance", 10)

#список файлов в архиве
letters = reader.list_files()
print("Файлы в архиве:", letters)
#папка для сортировки
BASE_DIR = "sorted_emails"
sorter = emailsort(base=BASE_DIR)

for filename in letters:
    extracted_path = reader.extract_to_temporary(filename)
    if not extracted_path:
        print(f"Ошибка извлечения файла из архива: {filename}")
        continue

    if reader.get_file_extension(filename) == "txt":
        letter = extractor.extract(extracted_path)
        if letter is not None:
            category = classifier.classify(letter)
            print(f"Письмо {filename} -> Категория: {category}")
            sorter.sort_one(extracted_path, category)
        else:
            print(f"Ошибка парсинга структуры письма: {filename}")
            sorter.sort_one(extracted_path, "inbox")
    else:
        # Если файл не txt, отправляем в спам 
        print(f"Пропущен файл (не txt): {filename} -> отправлен в spam")
        sorter.sort_one(extracted_path, "spam")

sorter.print_statistic()
reader.cleanup()

