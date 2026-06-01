from rules_classifier import *
from parser import LetterExtractor
from reader import Reader
from email_main import Letter
from actions import emailsort
import os

extractor = LetterExtractor()
reader = Reader(zip="inbox.zip", extractor=extractor)

#тут будут некоторые правила для классификации
classifier = main_classifier(default_category="inbox", stop_on_first_match=True)


#срочные письма
urgent_rule = keyword_rule(['срочно', 'быстро', 'незамедлительно', 'до конца дня', 'критично', 'дедлайн', 'сроки'], False, "both")
classifier.add_rule(urgent_rule, "urgent", 5)

#письма свыше прям от бога
boss_rule = sender_rule(['@company.ru', 'ceo@company.ru', 'boss@company.ru'], False)
classifier.add_rule(boss_rule, "from_boss", 1)

#важное и от босса
boss_urgent_rule = boss_rule & urgent_rule
classifier.add_rule(boss_urgent_rule, "BOSS_URGENT", 0)

#безопасность
security_rule = keyword_rule(['безопасность', 'security', 'уязвимость', 'vulnerability', 'пароль', 'password', 'взлом', 'угроза'], False, "both")
classifier.add_rule(security_rule, "security", 4)

#где требуется подтвердить что-то
confirmation_rule = keyword_rule(['подтвердите', 'verify', 'подтверждение', 'подтвердить', 'подписывайте'], False, "both")
classifier.add_rule(confirmation_rule, "need_confirmation", 6)

#где требуется согласовать(похоже на подтвердить, но отличается характером письма, там нужен был пароль для входа, тут разрешение что-то сделать)
approval_rule = keyword_rule(['согласовать', 'approve', 'одобрить', 'разрешите'], False, "both")
classifier.add_rule(approval_rule, "need_approval", 8)

#встречи и созвоны
meeting_rule = keyword_rule(['встреча', 'созвон', 'мит', 'совещание', 'встретиться', 'позвонить', 'запланировать'], False, "both")
classifier.add_rule(meeting_rule, "meeting", 9)

#проекты
project_rule = keyword_rule(['проект', 'задача', 'дедлайн', 'сроки', 'релиз', 'разработка', 'бэк'], False, "both")
classifier.add_rule(project_rule, "project", 10)


#финансы
finance_rule = sender_rule(['sberbank.ru', 'alfa.ru', 'tbank.ru', 'vtb.ru'], False)
classifier.add_rule(finance_rule, "finance", 20)

#письма-напоминания
reminder_rule = keyword_rule(['напоминание', 'не забудьте', 'reminder', 'задолженность'], False, "both")
classifier.add_rule(reminder_rule, "reminder", 21)

#стата по работе
report_rule = keyword_rule(['отчет', 'статистика', 'аналитика', 'метрики', 'kpi', 'показатели', 'данные'], False, "both")
classifier.add_rule(report_rule, "report", 30)

#вакансии
vacancy_rule = keyword_rule(['вакансия', 'резюме', 'собеседование', 'интервью', 'кандидат', 'найм', 'собес', 'оффер'], False, "both")
classifier.add_rule(vacancy_rule, "recruiting", 50)

#от роботов
auto_sender_rule = sender_rule(['noreply@', 'no-reply@', 'robot@', 'automail@'], False)
classifier.add_rule(auto_sender_rule, "auto_reply", 75)

#письма в спам
spam_rule = keyword_rule(['акция', 'выигрыш', 'распродажа', 'лотерея', 'скидка'], False, "both")
classifier.add_rule(spam_rule, "spam", 100000000)





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

