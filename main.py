import argparse
from message_parser import WhatsappChatParser, WhatsappMessage
import os
import unicodedata


def main(args):
    stop_words = read_wordlist_dir('stop_words')
    swear_words = read_wordlist_dir('swear_words')

    with open(args.filename, 'r') as rf:
        messages, people = WhatsappChatParser.parse(rf, args.dateformat)
    

def most_common_words(messages: list[WhatsappMessage], stop_words: set[str]):
    word_count = {}
    for m in messages:
        for word in m.content.split():
            if word in stop_words:
                continue
            if word in word_count:
                word_count[word] += 1
            else:
                word_count[word] = 1
    return {k: v for k, v in sorted(word_count, key=lambda item: item[1], reverse=True)}


def normalize_str(s: str):
    return ''.join(c for c in unicodedata.normalize('NFD', s.strip())
        if unicodedata.category(c) != 'Mn').lower()


def read_wordlist(filename: str):
    with open(filename, 'r') as rf:
        words = rf.read().splitlines()
    return set([normalize_str(w) for w in words])


def read_wordlist_dir(directory: str):
    words = set()
    for file in os.listdir(directory):
        words.update(read_wordlist(os.path.join(directory, file)))
    return words


def parse_args():
    parser = argparse.ArgumentParser()
    parser.add_argument('filename')
    parser.add_argument('--dateformat', default='%d/%m/%Y, %H:%M:%S')
    return parser.parse_args()
    

if __name__ == '__main__':
    main(parse_args())
