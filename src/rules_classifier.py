#правила классификации и её реализация Артем



#ВАЖНО - ЭТО ФАЙЛ С КЛАССАМИ ПРАВИЛ. САМИ ПРАВИЛА СОЗДАЮТСЯ В MAIN И В НИХ ПРОПИСЫВАЕТСЯ КОНКРЕТИКА, ТУТ ЖЕ АБСТРАКЦИЯ




from abc import ABC, abstractmethod
from typing import List, Tuple, Optional, Dict, Any
from dataclasses import dataclass
from enum import Enum
import re, logging
from .email_main import Email
#шаблонный класс для "подходит ли письмо под данное условие"
class rule(ABC):
    @abstractmethod
    def match(self, email):
        pass

#перегруз операторов для применения нескольких правил
class composite_rule(rule):
    def __init__(self, rules, logic):
        self.rules = rules
        self.logic = logic.upper()
    
    def matches(self, email):
        if self.logic == "AND":
            return all(rule.matches(email) for rule in self.rules)
        else:
            return any(rule.matches(email) for rule in self.rules)
    
#даем первому абстрактному классу эти операторы
def and_operator(self, other):
    return composite_rule([self, other], "AND")
def or_operator(self, other):
    return composite_rule([self, other], "OR")
rule.__and__ = and_operator
rule.__or__ = or_operator

#проверка отправителя на корректность
class sender_rule(rule):
    #patterns - список доменов, exact_match - если true, то ищем точное совпадение email, иначе подстроку
    def __init__(self, patterns, exact_match):
        self.patterns = [p.lower() for p in patterns]
        self.exact_match = exact_match
    #приводим для удобства к нижнему регистру и ишем или полное совпадение, или вхождение
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

#поиск ключевых слов для простой классификации
class keyword_rule(rule):
    #keywords - список ключевых слов, case_sensitive - учитывать ли регистр, target - где искать(subject, body, both)
    def __init__(self, keywords, case_sensitive, target):
        if case_sensitive:
            self.keywords = keywords
        else:
            self.keywords = [kw.lower() for kw in keywords]
        self.case_sensitive = case_sensitive
        self.target = target
    #берем текст и заголовок письма в нужном нам формате(с оставленным регистром или в нижнем)
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
    
#проверка регуляркой на наличие номеров, слов типо срочно и так далее
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
    
#добавляет приоритетность правилу
class priority_rule(rule):
    def __init__(self, rule, priority):
        self.rule = rule
        self.priority = priority
    
    def matches(self, email):
        return self.rule.matches(email)
    
#распределитель правил
class main_classifier(rule):
    #def_category - категория писем, что не подошли под правила, stop_on_first_match - остановка при первом мэтче
    def __init__(self, def_category, stop_on_first_match: bool):
        self._rules = []
        self.default_category = def_category
        self.stop_on_first_match = stop_on_first_match
        #self.logger = logging.getLogger(__name__)

    def add_rule(self, rule, category, priority):
        # Если правило имеет приоритет, учитываем его
        if hasattr(rule, 'priority'):
            priority = rule.priority
        self._rules.append((rule, category))
        #ленивая сортировка в одну строку
        self._rules.sort(key=lambda x: getattr(x[0], 'priority', 0), reverse=True)

    #на всякий и удаление правила
    def remove_rule(self, category: str, rule_index):
        if rule_index is not None:
            del self._rules[rule_index]
        else:
            self._rules = [(r, rule) for r, rule in self._rules if rule != category]

    #возвращает категорию письма по первому сработанному правилу
    def classify(self, email):
        matched_categories = []
        for rule, category in self._rules:
            try:
                if rule.matches(email):
                    #self.logger.debug(f"Rule matched: {rule.__class__.__name__} -- {category}")
                    matched_categories.append(category)
                    if self.stop_on_first_match:
                        return category
            except Exception as err:
                self.logger.error(f"ненашлось правило {rule}: {err}")
        #тут я поставил массив, потому что, в теории, может пригодиться иметь и остальные категории
        if matched_categories:
            return matched_categories[-1]
        else:
            return self.default_category
    #встроенная штука для нахожения количества(потом для подведения статы будет неплохо)
    def __len__(self):
        return len(self._rules)

#записываем правила в джсон файл и эта штука их распределяет
class rule_factory:
        @staticmethod
        def create(config):
            rule_type = config.get("type", "").lower()
            if rule_type == "keyword":
                return keyword_rule(
                    keywords=config["keywords"],
                    case_sensitive=config.get("case_sensitive", False),
                    target=config.get("target", "both")
                )
            elif rule_type == "sender":
                return sender_rule(
                    patterns=config["patterns"],
                    exact_match=config.get("exact_match", False)
                )
            elif rule_type == "regex":
                return regex_rule(
                    pattern=config["pattern"],
                    target=config.get("target", "both")
                )
            elif rule_type == "composite":
                sub_rules = [rule_factory.create(sub) for sub in config["rules"]]
                return composite_rule(
                    rules=sub_rules,
                    logic=config.get("logic", "AND")
                )
            else:
                raise ValueError(f"неизвестное правило: {rule_type}")
    




