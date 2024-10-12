import os
from collections import Counter

from message_parser import WhatsappMessage, Person, People


class AnalysisResults:
    def __init__(self, person: Person, words: dict[str, int], swear_words: dict[str, int]):
        self.person = person
        self.words = words
        self.swear_words = swear_words
        self.__sort_results()

    @staticmethod
    def __write_dict_to_file(filename: str, d: dict):
        with open(filename, 'w') as wf:
            for k, v in d.items():
                wf.write(f'{k}: {v}\n')
    
    @staticmethod
    def __sort_counter(d: dict[str, int]):
        return {k: v for k, v in sorted(d.items(), key=lambda x: x[1], reverse=True)}

    def __sort_results(self):
        self.words = AnalysisResults.__sort_counter(self.words)
        self.swear_words = AnalysisResults.__sort_counter(self.swear_words)

    def to_file(self, output_dir: str):
        path = os.path.join(output_dir, self.person.name)
        if not os.path.exists(path):
            os.makedirs(path)

        AnalysisResults.__write_dict_to_file(os.path.join(path, f'{self.person.name}_words.txt'), self.words)
        AnalysisResults.__write_dict_to_file(os.path.join(path, f'{self.person.name}_swear_words.txt'), self.swear_words)
    
    @staticmethod
    def combine(lst: list['AnalysisResults']):
        words = Counter()
        swear_words = Counter()
        
        for r in lst:
            words.update(r.words)
            swear_words.update(r.swear_words)
        
        return AnalysisResults(Person('Geral'), dict(words), dict(swear_words))


class MessagesAnalyzer:
    def __init__(self, stop_words: set[str], swear_words: set[str]):
        self.stop_words = stop_words
        self.swear_words = swear_words
    
    @staticmethod
    def __register_in_counter(counter: dict[str, int], word: str):
        if word in counter:
            counter[word] += 1
        else:
            counter[word] = 1
    
    def analyze(self, messages: list[WhatsappMessage], people: People):
        counters = {p.name: {
            'words': {},
            'swear_words': {}   
        } for p in people.people}
        
        for m in messages:
            for word in m.content.split():
                if word in self.stop_words:
                    continue
                
                MessagesAnalyzer.__register_in_counter(counters[m.sender.name]['words'], word)
                if word in self.swear_words:
                    MessagesAnalyzer.__register_in_counter(counters[m.sender.name]['swear_words'], word)
        
        results = []
        for c in counters:
            results.append(AnalysisResults(people.get(c), counters[c]['words'], counters[c]['swear_words']))
            
        return results