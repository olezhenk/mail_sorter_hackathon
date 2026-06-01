#правила классификации и её реализация Артем



#ВАЖНО - ЭТО ФАЙЛ С КЛАССАМИ ПРАВИЛ. САМИ ПРАВИЛА СОЗДАЮТСЯ В MAIN И В НИХ ПРОПИСЫВАЕТСЯ КОНКРЕТИКА, ТУТ ЖЕ АБСТРАКЦИЯ

from abc import ABC, abstractmethod
from typing import List, Tuple, Optional, Dict, Any
import re, logging
from email_main import Letter
#шаблонный класс для создания базовых правил, то есть "подходит ли письмо под данное условие"
class rule(ABC):
    @abstractmethod
    def matches(self, email):
        pass

#перегруз операторов и и или для применения нескольких правил к письму одновременно
class composite_rule(rule):
    def __init__(self, rules, logic):
        self.rules = rules
        self.logic = logic.upper()
    
    def matches(self, email):
        if self.logic == "AND":
            return all(rule.matches(email) for rule in self.rules)
        else:
            return any(rule.matches(email) for rule in self.rules)
    
#даем абстрактному правилу эти операторы
def and_operator(self, other):
    return composite_rule([self, other], "AND")
def or_operator(self, other):
    return composite_rule([self, other], "OR")
rule.__and__ = and_operator
rule.__or__ = or_operator

#праивло для проверки отправителя на корректность
class sender_rule(rule):
    #patterns это список доменов, exact_match это условие, нужно ли найти точное совпадение, или хватит вхождения
    def __init__(self, patterns, exact_match):
        self.patterns = [p.lower() for p in patterns]
        self.exact_match = exact_match
    #приводим для удобства к нижнему регистру и ишем вхождение/совпадение
    def matches(self, email):
        sender_lower = email.sender.lower()
        for pattern in self.patterns:
            if self.exact_match:
                if sender_lower == pattern:
                    return True
            else:
                if pattern in sender_lower:
                    return True
        return False

#правило по поиску ключевых слов(срочно, быстро, незамедлительно и любые другие)
class keyword_rule(rule):
    #keywords это ключевые слова, case_sensitive - нужен ли регистр, target - где искать(название, письмо или сразу и там, и там)
    def __init__(self, keywords, case_sensitive, target):
        if case_sensitive:
            self.keywords = keywords
        else:
            self.keywords = [kw.lower() for kw in keywords]
        self.case_sensitive = case_sensitive
        self.target = target
    #берем текст и заголовок письма в нужном регистре и ищем ключи
    def matches(self, email):
        text_parts = []
        if self.target in ("subject", "both"):
            if self.case_sensitive:
                subject = email.subject
            else:
                subject = email.subject.lower()
            text_parts.append(subject)
        if self.target in ("body", "both"):
            if self.case_sensitive:
                body = email.body_plain
            else:
                body = email.body_plain.lower()
            text_parts.append(body)
        combined_text = " ".join(text_parts)
        return any(kw in combined_text for kw in self.keywords)


'''   
ПОКА ХЗ, ОСТАВЛЯТЬ ЛИ ЭТО
#проверка регуляркой на наличие номеров, чисел и других
class regex_rule(rule):
    def __init__(self, pattern, target):
        self.regex = re.compile(pattern)
        self.target = target
        
    def matches(self, email):
        text = ""
        if self.target in ("subject", "both"):
            text += email.subject + " "
        if self.target in ("body", "both"):
            text += email.body_plain
        return bool(self.regex.search(text))
'''
    
#добавляет правилу приоритетность(например, если ключевое слово важнее номера в письме)
class priority_rule(rule):
    def __init__(self, rule, priority):
        self.rule = rule
        self.priority = priority
    
    def matches(self, email):
        return self.rule.matches(email)
    
#распределитель всех правил
class main_classifier:
    #def_category вернется, когда ни одно правило не подойдет под наше письмо, stop_on_first_match это бул переменная, если нужна остановка при первом мэтче
    def __init__(self, default_category, stop_on_first_match):
        self._rules = []
        self.default_category = default_category
        self.stop_on_first_match = stop_on_first_match
        self.logger = logging.getLogger(__name__)

    def add_rule(self, rule, category, priority):
        #при добавлении учитываем приоритет(если он есть)
        if hasattr(rule, 'priority'):
            priority = rule.priority
        self._rules.append((rule, category))
        #ленивая сортировка в одну строку
        self._rules.sort(key=lambda x: getattr(x[0], 'priority', 0))

    #на всякий случай и возможность удалить правило
    def remove_rule(self, category, index):
        if index is not None:
            del self._rules[index]
        #если нет конкретного индекса, то мы хотим удалить все правила из данной категории(например, не по ключевому слову срочно, а вообще все по ключевым словам)
        else:
            self._rules = [(rule, categ) for rule, categ in self._rules if categ != category]

    #возвращает категорию письма по первому сработанному правилу
    def classify(self, email):
        matched_categories = []
        for rule, category in self._rules:
            try:
                if rule.matches(email):
                    matched_categories.append(category)
                    if self.stop_on_first_match:
                        return category
            except Exception as err:
                self.logger.error(f"не нашлось правило {rule}: {err}")
        #тут я поставил массив, потому что, в теории, может пригодиться иметь и остальные категории
        if matched_categories:
            return matched_categories[-1]
        else:
            return self.default_category
    #встроенная штука для нахожения количества(потом для подведения статы будет неплохо)
    def __len__(self):
        return len(self._rules)
    
