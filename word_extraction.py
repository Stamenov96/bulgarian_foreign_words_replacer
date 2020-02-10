import stemmer
import tokenizer
import transliteration


def load_synonims(synonims_file):
    synonims = {}
    with open(synonims_file, 'r') as file_with_synonims:
        for line in file_with_synonims:
            words = line.rstrip('\n').lower().split(" ")
            synonims[words[0]] = words[1:]
    return synonims


def load_bulgarian_words(bulgarian_words_file):
    bulgarian_words = []
    with open(bulgarian_words_file, 'r') as bg_words_file:
        for line in bg_words_file:
            bulgarian_words.append(line.rstrip("\n"))
    return bulgarian_words


def load_english_word(english_words_file):
    english_words = []
    with open(english_words_file, 'r') as en_words_file:
        for line in en_words_file:
            english_words.append(line.rstrip("\n"))
    return english_words


if __name__ == '__main__':
    stem = stemmer.Stemmer()
    tokens = tokenizer.tokenize_text("assets/input.txt")
    tokens = list(set(tokens))

    synonims = load_synonims("assets/synonims.txt")
    bulgarian_words = load_bulgarian_words("assets/bulgarianwords.txt")

    replacing_parits = {}

    for word in synonims.keys():
        value = synonims[word]
        synonims.pop(word)
        synonims[stem.stem_word(word)] = value

    suggestions = {}

    for token in tokens:
        stemmmed_token = stem.stem_word(token)
        match = synonims.get(stemmmed_token)
        if match:
            print(f'we suggest {token} to be replaced with {match}')
