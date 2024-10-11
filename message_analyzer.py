from message_parser import WhatsappMessage, Person, People


class AnalysisResults:
    def __init__(self, person: Person, words: dict[str, int], swear_words: dict[str, int]):
        self.person = person
        self.words = words
        self.swear_words = swear_words


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
    
    @staticmethod
    def __sort_counter(d: dict[str, int]):
        return {k: v for k, v in sorted(d.items(), key=lambda x: x[1], reverse=True)}

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
        
        for mycounters in counters.values():
            for counter in mycounters:
                mycounters[counter] = MessagesAnalyzer.__sort_counter(mycounters[counter])
        
        results = []
        for c in counters:
            results.append(AnalysisResults(people.get(c), counters[c]['words'], counters[c]['swear_words']))
            
        return results