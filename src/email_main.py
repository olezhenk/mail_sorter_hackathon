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
