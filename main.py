import re
from datetime import datetime
from dateutil import parser as auto_date_parser
import argparse


def main(args):
    people = People()
    messages = []

    # matches invisible control characters
    pattern = r'[\u200E\u200F\u202A-\u202E]'
    
    with open(args.filename, 'r') as rf:
        messages_raw = re.sub(pattern, '', rf.read())
    
    for message in messages_raw:
        messages.append(Message.parse(message, people))
    
    # FIX: messages with explicit linebreaks \n are parsed as new messages after \n


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


class Message:
    def __init__(self, date: datetime, sender: Person, content: str):
        self.date = date
        self.sender = sender
        self.content = content

    @staticmethod
    def parse(message: str, people: People, pattern: str = r'\[(.*?)\] (.*?): (.*)'):
        match = re.match(pattern, message, flags=re.UNICODE)

        date_str = match.group(1)  # date and time
        contact = match.group(2)   # contact name
        message = match.group(3)   # message content

        try:
            parsed_date = datetime.strptime(date_str, "%d/%m/%Y, %H:%M:%S")
        except ValueError:
            parsed_date = auto_date_parser.parse(date_str)
        
        person = people.get(contact) or people.add(Person(contact))
        return Message(parsed_date, person, message)
    
    def __str__(self):
        return f"{self.date} - {self.sender.name}: {self.content}"


def parse_args():
    parser = argparse.ArgumentParser()
    parser.add_argument('filename')
    return parser.parse_args()
    

if __name__ == '__main__':
    main(parse_args())
