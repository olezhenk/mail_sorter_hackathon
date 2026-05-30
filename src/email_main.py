#экземляр (модель письма) Лена Руссу
class Email:
    def __init__(self):
        self.message_id = ""
        self.from_email = ""
        self.to = ""
        self.subject = ""
        self.text = ""
        self.date = ""
        self.files = []

    def add_file(self, filename):
        self.files.append(filename)
        print(f"Добавлен файл: {filename}")

    def show_info(self):
        print("=== ИНФОРМАЦИЯ О ПИСЬМЕ ===")
        print(f"ID письма: {self.message_id}")
        print(f"От: {self.from_email}")
        print(f"Кому: {self.to}")
        print(f"Тема: {self.subject}")
        print(f"Текст: {self.text}")
        print(f"Дата: {self.date}")
        if self.files:
            print(f"Файлы: {', '.join(self.files)}")
        else:
            print("Файлы: нет")
        print("=========================")
