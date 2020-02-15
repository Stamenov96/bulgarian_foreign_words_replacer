import string
from nltk.tokenize import word_tokenize


def tokenize_text(input_file_path):
    with open(input_file_path, 'rt') as input_file:
        text = input_file.read()

    # split into words
    tokens = word_tokenize(text)
    # convert to lower case
    tokens = [w.lower() for w in tokens]
    # remove punctuation
    table = str.maketrans('', '', string.punctuation)
    stripped = [w.translate(table) for w in tokens]
    # remove remaining tokens that are not alphabetic
    words = [word for word in stripped if word.isalpha()]
    # filter out stop words
    stop_words = read_stop_words("assets/stopwords.txt")
    words = [w for w in words if w not in stop_words]
    return words


def read_stop_words(stop_words_file_path):
    stop_words = []
    with open(stop_words_file_path, 'r') as stop_words_file:
        for line in stop_words_file:
            stop_words.append(line.rstrip('\n'))
    return stop_words
