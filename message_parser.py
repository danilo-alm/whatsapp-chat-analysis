import re
from datetime import datetime
from dateutil import parser as auto_date_parser
from typing import TextIO
import unicodedata


class Person:
    def __init__(self, name):
        self.name = name


class People:
    def __init__(self):
        self.people = []
    
    def add(self, person):
        self.people.append(person)
        return person
    
    def get(self, name):
        for person in self.people:
            if person.name == name:
                return person
    
    def check(self, name):
        return self.get(name) is not None 


class WhatsappMessage:
    def __init__(self, date: datetime, sender: Person, content: str):
        self.date = date
        self.sender = sender
        self.content = content
    
    def __str__(self):
        return f"{self.date} - {self.sender.name}: {self.content}"


class WhatsappMessageParser:
    def __init__(self, date_format: str, group: bool = False):
        self.date_format = date_format
        self.people = People()
        self.pattern = r'(\d{2}/\d{2}/\d{4} \d{2}:\d{2}) - (.*?): (.*)' if group else r'\[(.*?)\] (.*?): (.*)'
    
    def __normalize(s: str):
        return ''.join(c for c in unicodedata.normalize('NFD', s)
            if unicodedata.category(c) != 'Mn').lower()

    def parse(self, message: str):
        match = re.match(self.pattern, message, flags=re.UNICODE)

        if not match:
            return

        date_str = match.group(1)
        contact = match.group(2)
        message = match.group(3)

        try:
            parsed_date = datetime.strptime(date_str, self.date_format)
        except ValueError:
            parsed_date = auto_date_parser.parse(date_str)

        message = WhatsappMessageParser.__normalize(message)
        person = self.people.get(contact) or self.people.add(Person(contact))

        return WhatsappMessage(parsed_date, person, message)


class WhatsappChatParser:
    @staticmethod
    def parse(file: TextIO, date_format: str, group: bool = False):
        wmparser = WhatsappMessageParser(date_format, group)
        messages: list[WhatsappMessage] = []

        buffer = None
        last_message = None

        while True:
            buffer = file.readline()
            if not buffer:
                break

            buffer = re.sub(r'[\u200E\u200F\u202A-\u202E]', '', buffer)
            parsed = wmparser.parse(buffer)

            if parsed:
                messages.append(parsed)
                last_message = parsed
            else:
                if last_message:
                    last_message.content += '\n' + buffer

        return messages, wmparser.people