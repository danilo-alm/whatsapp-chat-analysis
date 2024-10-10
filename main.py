import argparse
from message_parser import WhatsappChatParser
import os
import unicodedata


def main(args):
    with open(args.filename, 'r') as rf:
        messages, people = WhatsappChatParser.parse(rf, args.dateformat)


def normalize_str(s: str):
    return ''.join(c for c in unicodedata.normalize('NFD', s.strip())
        if unicodedata.category(c) != 'Mn').lower()


def get_stop_words(directory: str):
    stop_words = set()
    for file in os.listdir(directory):
        with open(os.path.join(directory, file), 'r') as rf:
            words = rf.read().splitlines()
        stop_words.update([normalize_str(w) for w in words])
    return stop_words


def parse_args():
    parser = argparse.ArgumentParser()
    parser.add_argument('filename')
    parser.add_argument('--dateformat', default='%d/%m/%Y, %H:%M:%S')
    return parser.parse_args()
    

if __name__ == '__main__':
    main(parse_args())
