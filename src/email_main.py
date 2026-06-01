class Letter:
    def __init__(self, from_email, to, subject, text, date, files):
        self.from_email = from_email
        self.to = to
        self.subject = subject
        self.text = text
        self.date = date
        self.files = files


    def __str__(self):
        print(f"From: {self.from_email}\nTo: {self.to}\nSubject: {self.subject}\nDate: {self.date}\nText: {self.text[:50]}...\nFiles: {self.files}")