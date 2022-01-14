import os
import random
import math

from deep_translator import GoogleTranslator


def shuffled(arr):
    random.shuffle(arr)
    return arr


def request_words_dict():
    words_dict = {}
    dictionary_path = os.path.join(os.path.dirname(__file__), "dictionary")

    for path, dirs, files in os.walk(dictionary_path):
        for file in files:
            words_type = file.split('#')[0]
            words = open(os.path.join(path, file)).read().split(' ')
            words_dict.setdefault(words_type, []).extend(words)

    for words in words_dict.values():
        random.shuffle(words)

    return words_dict


def generate_text(words_dict, sentence_count: int, words_in_sentence: int):
    sentences = []

    for i in range(sentence_count):
        _slice = slice(i * words_in_sentence, (i + 1) * words_in_sentence)

        nouns = shuffled(words_dict["nouns"][_slice])
        adjectives = shuffled(words_dict["adjectives"][_slice])
        verbs = shuffled(words_dict["verbs"][_slice])

        words = []
        for j in range(words_in_sentence):
            words.append(adjectives[j])
            words.append(nouns[j])
            words.append(verbs[j])

        words.extend(words_dict.get("additional", []))

        dots_count = math.ceil(words_in_sentence / 2)
        words.extend(shuffled([words_dict["dots"][j] for j in range(dots_count)]))

        sentences.append(' '.join(shuffled(words)))

    return '.\n\n'.join(sentences)


def translate_a_few_times(text):
    translators = [
        GoogleTranslator("en", "ar"),
        GoogleTranslator("ar", "chinese (traditional)"),
        GoogleTranslator("chinese (traditional)", "ru")
    ]

    for translator in translators:
        text = translator.translate(text)

    return text


def main():
    import sys

    sentence_count = 30
    words_in_sentence = 5
    words_dict = request_words_dict()

    if len(sys.argv) > 1:
        words_dict["additional"] = sys.argv[1:]

    text = generate_text(words_dict, sentence_count, words_in_sentence)
    text = translate_a_few_times(text)

    print(text)


if __name__ == '__main__':
    main()
