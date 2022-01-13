import requests
import random
import math

from deep_translator import GoogleTranslator


def shuffled(arr):
    random.shuffle(arr)
    return arr


def request_words_dict(sentences: int, words_in_sentence: int):
    random_word_url_base = "https://random-word-form.herokuapp.com/random"

    nouns = []
    adjectives = []

    for _ in range(sentences):
        # Сервер каждый раз возвращает слова начинающиеся на одинаковую букву, по-этому
        # по запросу на предложение

        nouns.extend(requests.get(f"{random_word_url_base}/noun?count={words_in_sentence}").json())
        adjectives.extend(requests.get(f"{random_word_url_base}/noun?count={words_in_sentence}").json())

    return {
        "nouns": nouns,
        "adjectives": adjectives,
        "verbs": shuffled(open("verbs.txt").read().replace('\t', ' ').replace('\n', ' ').split(' ')),
        "dots": shuffled(list('.' * 5 + ',' * 5 + '!' * 2))
    }


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

    sentence_count = 4
    words_in_sentence = 5
    words_dict = request_words_dict(sentence_count, words_in_sentence)

    if len(sys.argv) > 1:
        words_dict["additional"] = sys.argv[1:]

    text = generate_text(words_dict, sentence_count, words_in_sentence)
    text = translate_a_few_times(text)

    print(text)


if __name__ == '__main__':
    main()
