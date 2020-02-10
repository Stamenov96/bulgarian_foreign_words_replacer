import stemmer
import tokenizer
import transliteration
import levenstein


def load_synonims(synonims_file):
    synonyms = {}
    with open(synonims_file, 'r') as file_with_synonims:
        for line in file_with_synonims:
            words = line.rstrip('\n').lower().split(" ")
            synonyms[words[0]] = words[1:]
    return synonyms


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


def check_and_get_match_for_synonyms(checked_word, synonyms):
    stemmmed_word = stem.stem_word(checked_word)
    match = synonyms.get(stemmmed_word)
    return match


def is_bg_word(checked_word, bul_words):
    for bw in bul_words:
        if bw == checked_word:
            return True
    return False


def check_for_english_alternative(checked_word, eng_words):
    transliterated_word = transliteration.transliterate(checked_word)
    for ew in eng_words:
        levenstein_ratio = levenstein.levenshtein_ratio_and_distance(ew, transliterated_word, ratio_calc=True)
        if levenstein_ratio > 0.8:
            print(f'---en---{checked_word}---transliterated as---{transliterated_word} --- is ---{ew}')


if __name__ == '__main__':
    stem = stemmer.Stemmer()
    tokens = tokenizer.tokenize_text("assets/input.txt")
    tokens = list(set(tokens))

    foreign_synonyms = load_synonims("assets/synonims.txt")
    bg_words = load_bulgarian_words("assets/bulgarianwords.txt")
    en_words = load_bulgarian_words("assets/englishWords.txt")

    for word in foreign_synonyms.keys():
        value = foreign_synonyms[word]
        foreign_synonyms.pop(word)
        foreign_synonyms[stem.stem_word(word)] = value

    suggestions = {}
    bg_words = []

    for token in tokens:
        if is_bg_word(checked_word=token, bul_words=bg_words):
            print(f'---BG---{token}')
            continue
        else:
            synonym = check_and_get_match_for_synonyms(checked_word=token, synonyms=foreign_synonyms)
            if synonym:
                suggestions[token] = synonym
                print(f'---synonym---{synonym}')
                continue
            else:
                check_for_english_alternative(token, en_words)

    print("-----suggestions-----")
    print(suggestions)
    print("-----bg words-----")
    print(len(bg_words))
