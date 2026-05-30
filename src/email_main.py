class Letter:
    def __init__(self, from_email, to, subject, text, date, files):
        self.from_email = from_email
        self.to = to
        self.subject = subject
        self.text = text
        self.date = date
        self.files = files