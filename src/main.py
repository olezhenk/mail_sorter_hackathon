from rules_classifier import *
from parser import LetterExtractor
from reader import Reader
from email_main import Letter
from actions import emailsort
extractor = LetterExtractor()
reader = Reader(zip="inbox.zip", extractor=extractor)
#тут ниже будут некоторые правила для классификации
classifier = main_classifier(default_category="inbox", stop_on_first_match=True)
#письма свыше прям от бога
boss_rule = sender_rule(['@company.ru', 'ceo@company.ru', 'boss@company.ru'], False)
classifier.add_rule(boss_rule, "from_boss", 1)
#письма в спам
spam_rule = keyword_rule(['акция', 'выигрыш', 'распродажа', 'лотерея', 'скидка'], False, "both")
classifier.add_rule(spam_rule, "spam", 100)
#срочные письма
urgent_rule = keyword_rule(['срочно', 'быстро', 'незамедлительно', 'до конца дня', 'критично'], False, "both")
classifier.add_rule(urgent_rule, "urgent", 5)
#финансы
finance_rule = sender_rule(['sberbank.ru', 'alfa.ru', 'tbank.ru', 'vtb.ru'], False)
classifier.add_rule(finance_rule, "finance", 10)


#нужно подумать, добавлять ли регулярку и что на нее добавлять(номера телефонов там и так далее)
#список файлов  вархиве

letters = reader.list_files()
print(letters)
#создаем папку для прошедших проверку хз как еще сфомулировать
sorter = emailsort(base="sorted_emails")
email_to_sort = []
for filename in letters:
    if reader.get_file_extension(filename) == "txt":
        letter = reader.read_file(filename)
        if letter is not None:
            category = classifier.classify(letter)
            print("Письмо №", letters.index(filename) + 1, "категория письма: ", category)
            #добавка письма и пути к нему в список прошедших проверку писем
            email_to_sort.append((filename, letter))
        else:
            print(f"oшибка чтения: {filename}")
    else:
        print(f"пропущен файл(не txt): {filename}")
        sorter.sort_one(filename, "spam")

sorter.sort_all(email_to_sort, classifier)
sorter.print_statistic()
reader.cleanup()
