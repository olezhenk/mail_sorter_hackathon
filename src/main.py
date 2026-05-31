from rules_classifier import *
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