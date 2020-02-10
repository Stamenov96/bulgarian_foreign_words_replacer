import re


class Stemmer:
    def __init__(self):
        self.vocals = re.compile(r'[^аъоуеияю]*[аъоуеияю]')
        self.p = re.compile(r'([а-я]+)\s==>\s([а-я]+)\s([0-9]+)')
        self.stem_boundary = 1
        self.stemming_rules = self.load_stemming_rules()

    def load_stemming_rules(self):
        path_to_files = []
        path_to_files.append("assets/stemming_rules/stem_rules_context_1.txt")
        path_to_files.append("assets/stemming_rules/stem_rules_context_2.txt")
        path_to_files.append("assets/stemming_rules/stem_rules_context_3.txt")
        steaming_rules = {}

        for path in path_to_files:
            with open(path, encoding='utf8', mode='r') as rules_file:
                for line in rules_file:
                    rule_line = line.rstrip('\n')
                    m = self.p.search(rule_line)
                    if m:
                        if len(m.groups()) == 3:
                            if int(m.group(3)) > self.stem_boundary:
                                steaming_rules[m.group(1)] = m.group(2)
        return steaming_rules

    def stem_word(self, word):
        m = self.vocals.search(word)
        if not m:
            return word
        for i in range(m.end()+1, len(word)):
            suffix = word[i:]
            suffix = self.stemming_rules.get(suffix)
            if suffix:
                return word[0:i]+suffix
        return word


if __name__ == '__main__':
    new_stemmer = Stemmer()
