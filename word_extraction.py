import stemmer
import tokenizer
import transliteration
import levenstein


def load_synonims(synonims_file):
    synonyms = {}
    with open(synonims_file, 'r') as file_with_synonims:
        for line in file_with_synonims:
            words = line.rstrip('\n').lower().split("-")
            synonyms[words[0]] = words[1].split(",")
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
        if bw[0] == checked_word[0]:
            if bw == checked_word:
                return True
    return False


def check_for_english_alternative(unwords, eng_words):
    possible_replace_words = set()
    for uword in unwords:
        transliterated_word = transliteration.transliterate(uword)
        for ew in eng_words:
            if levenstein.levenshtein_ratio_and_distance(transliterated_word, ew, ratio_calc=True) > 0.9:
                # print(f'---bg---{uword}---transliterated as---{transliterated_word} --- is close to---{ew}')
                possible_replace_words.add(uword)
    return possible_replace_words


def check_with_levenstein(uwords, words):
    for bw in words:
        for uword in uwords:
            if uword[0] == bw[0]:
                if levenstein.levenshtein_ratio_and_distance(uword, bw, True) > 0.9:
                    # print(f'{uword} is recognized as {bw}')
                    uwords.remove(uword)


def print_suggestions(replace_suggestions):
    for k, v in replace_suggestions.items():
        print(f'{k} ---> {v[0]} други възможности за подмяна са думите {",".join(v[1:])}')


def process_tokens(text_tokens):
    words_suggestions = {}
    unknown_processed_words = set()
    for token in text_tokens:
        if is_bg_word(checked_word=token, bul_words=bg_words):
            continue
        else:
            synonym = check_and_get_match_for_synonyms(checked_word=token, synonyms=foreign_synonyms)
            if synonym:
                words_suggestions[token] = synonym
            else:
                unknown_processed_words.add(token)
    return words_suggestions, list(unknown_processed_words)


if __name__ == '__main__':
    stem = stemmer.Stemmer()

    tokens = tokenizer.tokenize_text("assets/input.txt")
    tokens = list(set(tokens))
    print(f'Нашият входен текст съдържа {len(tokens)} значими думи')

    print('Зареждаме чуждиците и техните синоними ')
    foreign_synonyms = load_synonims("assets/synonyms.txt")
    print('Зареждаме корпусът с български думи')
    bg_words = load_bulgarian_words("assets/bg_words.txt")
    print('Зареждаме корпусът с английски думи')
    en_words = load_bulgarian_words("assets/en_words.txt")

    for word in foreign_synonyms.keys():
        value = foreign_synonyms[word]
        foreign_synonyms.pop(word)
        foreign_synonyms[stem.stem_word(word)] = value

    print('Започваме да обхождаме и проверяваме думите на входния текст')
    suggestions, unknown_words = process_tokens(tokens)
    print('След първоначална обработка предлагаме следната замяна на думи:')
    print_suggestions(suggestions)
    print(f'След първоначална обработка имаме {len(unknown_words)} неизвестни думи')
    print('Започва допълнителна обработка на думите, ще проверим за думи със случайни правописни грешки')
    check_with_levenstein(unknown_words, bg_words)
    print(f'След допълнителната обработка броят на неизвестние ни думите е {len(unknown_words)}')
    print(f'Сега ще проверим дали в неизвестните ни думи има жудици, които можем да открием, чрез транслитерация')
    new_foreigns = check_for_english_alternative(unknown_words, en_words)
    print('След транслитерацията предполагаме, че следните думи са чуждици и имат български синоними:')
    print(",".join(new_foreigns))
    print(f'Борй на неизвестние думи: {len(unknown_words)-len(new_foreigns)}')