import argparse
import random

from .base import StageBase, register_stage

SENTENCE_STRUCTURES = [
    ["Obj", "Verb", "Obj"],
    ["Obj", "Verb", "Adj"],
    ["Obj", "Verb"],
    ["Adj", "Verb"]
]

SENTENCE_TRANSFORMS = {
    "Obj": [["Adj", "Obj"]],
    'Adj': [["Adj", 'Adj']]
}
SENTENCE_TRANSFORMS_CHANCES = {
    "Obj": [40],
    'Adj': [10]
}

SENTENCE_CONJUGATIONS = (
    [", ", ": ", "- ", ' ', ' and ', ' or ', ' because ', ' after ', ' before '],
    [70, 10, 10, 30, 20, 20, 20, 20, 20]    # Weights
)

SENTENCE_SEPARATOR = (
    [".", "!", "?"],
    [60, 20, 20]    # Weights
)


def _enumerate_structure(text_structure):
    for nested_structure in text_structure:
        if not isinstance(nested_structure, list):
            continue

        for child in _enumerate_structure(nested_structure):
            yield child

    yield text_structure


def _enumerate_structure_parts(text_structure):
    for nested_structure in _enumerate_structure(text_structure):
        for i, part in enumerate(nested_structure):
            if not isinstance(part, list):
                yield i, nested_structure, part


def _enchant_text_structure(text_structure):
    for i, structure, part in _enumerate_structure_parts(text_structure):
        if part not in SENTENCE_TRANSFORMS:
            continue

        transforms = SENTENCE_TRANSFORMS[part]
        chances = SENTENCE_TRANSFORMS_CHANCES[part]

        for j, transform in enumerate(transforms):
            if chances[j] >= random.randint(0, 100):
                structure[i] = transforms[j].copy()


@register_stage("structure")
class Structure(StageBase):
    _parser = argparse.ArgumentParser(
        usage="xylophone -s structure --obj OBJECTIVES --adj ADJECTIVES --verb VERBS "
              "[--sub_sentence_count SUB_SENTENCE_COUNT] [--sentence_count SENTENCE_COUNT] [--seed SEED]",
        description="Generate a sentence structure",
        add_help=False)

    _parser.add_argument("--obj", dest="objectives", type=str, required=True)
    _parser.add_argument("--adj", dest="adjectives", type=str, required=True)
    _parser.add_argument("--verb", dest="verbs", type=str, required=True)

    _parser.add_argument("--sub_sentence_count", dest="sub_sentence_count", default=2, type=int)
    _parser.add_argument("--sentence_count", dest="sentence_count", default=1, type=int)
    _parser.add_argument("--seed", dest="seed", default=None, type=int, help="PRNG seed.")

    def __init__(self, *args):
        self._args, self._unknown_args = self._parser.parse_known_args(args)

        self._random = random.Random(self._args.seed)
        self._sub_sentence_count = self._args.sub_sentence_count
        self._sentence_count = self._args.sentence_count

        self._words_dict = {
            "Obj": self._args.objectives.split(' '),
            "Adj": self._args.adjectives.split(' '),
            "Verb": self._args.verbs.split(' ')
        }

    def process(self) -> [str]:
        text_structure = self._generate_text_structure()
        _enchant_text_structure(text_structure)
        return [*self._unknown_args, self._apply_words(text_structure)]

    def _generate_text_structure(self):
        text_structure = []

        for _ in range(self._sentence_count):
            for i in range(self._sub_sentence_count):
                structure = self._random.choice(SENTENCE_STRUCTURES).copy()
                text_structure.append(structure)

                if i != self._sub_sentence_count - 1:
                    conjugation = self._random.choices(*SENTENCE_CONJUGATIONS, k=1)[0]
                    text_structure.append(conjugation)

            separator = self._random.choices(*SENTENCE_SEPARATOR, k=1)[0]
            text_structure.append(separator)

        return text_structure

    def _apply_words(self, text_structure: [str]) -> str:
        def setup_words(structure):
            for i, structure, part in _enumerate_structure_parts(structure):
                if part in self._words_dict:
                    structure[i] = self._random.choice(self._words_dict[part])

        def connect_words(structure):
            for j, part in enumerate(structure):
                if not isinstance(part, str):
                    structure[j] = connect_words(part)

            return ' '.join(structure)

        copy_structure = text_structure.copy()
        setup_words(copy_structure)
        return connect_words(copy_structure)

    @staticmethod
    def help() -> str:
        return Structure._parser.format_help()
