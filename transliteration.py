def rules(letter):
    letter = letter.lower()
    switcher = {
        " ": " ",
        "а": "a",
        "б": "b",
        "в": "v",
        "г": "g",
        "д": "d",
        "е": "e",
        "ж": "zh",
        "з": "z",
        "и": "i",
        "й": "y",
        "к": "k",
        "л": "l",
        "м": "m",
        "н": "n",
        "о": "o",
        "п": "p",
        "р": "r",
        "с": "s",
        "т": "t",
        "у": "u",
        "ф": "f",
        "х": "h",
        "ц": "ts",
        "ч": "ch",
        "ш": "sh",
        "щ": "sht",
        "ъ": "a",
        "ь": "y",
        "ю": "yu",
        "я": "ya",
        "дж": "dzh",
        "дз": "dz",
        "ьо": "yo",
        "йо": "yo",
        "ия": "ia",
    }
    return switcher.get(letter, "err")


def transliterate(bulgarian_word):
    return_string = ""
    tmp = ""
    flag = False
    for i in range(0, len(bulgarian_word)):
        if flag is True:
            flag = False
            continue

        if (bulgarian_word[i] is 'д' and (bulgarian_word[i+1] is 'з' or bulgarian_word[i+1] is 'ж')) or (bulgarian_word[i] is 'ь' and bulgarian_word[i+1] is 'o') or (bulgarian_word[i] is 'й' and bulgarian_word[i+1] is 'o') or (bulgarian_word[i] is 'и' and bulgarian_word[i+1] is 'я'):
            tmp = bulgarian_word[i] + bulgarian_word[i+1]
            flag = True
        else:
            tmp = bulgarian_word[i]

        english_letter = rules(tmp)
        if(english_letter is "err"):
            return_string = "Error"
            break
        else:
            return_string += english_letter
    return return_string
