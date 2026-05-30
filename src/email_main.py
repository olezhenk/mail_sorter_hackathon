#экземляр (модель письма) Лена Руссу
from dataclasses import dataclass
from typing import Optional

@dataclass
class Email:
    message_id: str
    from_email: str
    to: str
    subject: str
    text: str
    html: Optional[str] = None
    date: Optional[str] = None
    files: list = None
