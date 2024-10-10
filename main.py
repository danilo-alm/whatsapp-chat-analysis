import argparse
from message_parser import WhatsappChatParser


def main(args):
    with open(args.filename, 'r') as rf:
        messages, people = WhatsappChatParser.parse(rf, args.dateformat)


def parse_args():
    parser = argparse.ArgumentParser()
    parser.add_argument('filename')
    parser.add_argument('--dateformat', default='%d/%m/%Y, %H:%M:%S')
    return parser.parse_args()
    

if __name__ == '__main__':
    main(parse_args())
