import argparse
import os
import unicodedata

from message_parser import WhatsappChatParser 
from message_analyzer import MessagesAnalyzer, AnalysisResults


def main(args):
    messages, people = WhatsappChatParser.parse(open(args.filename, 'r'), args.dateformat, args.group)
    
    analyzer: list[AnalysisResults] = MessagesAnalyzer(
        stop_words=read_wordlist_dir('stop_words'),
        swear_words=read_wordlist_dir('swear_words')
    )

    results: list[AnalysisResults] = analyzer.analyze(messages, people)
    for r in results:
        r.to_file(args.output_dir)
    
    AnalysisResults.combine(results).to_file(args.output_dir)


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
    parser.add_argument('--output-dir', default='results')
    parser.add_argument('-g', '--group', action='store_true')
    return parser.parse_args()
    

if __name__ == '__main__':
    main(parse_args())
