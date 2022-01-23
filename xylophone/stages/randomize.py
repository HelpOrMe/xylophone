import math
import random

from .base import StageBase, ArgumentParser, register_stage


@register_stage("randomize")
class Randomize(StageBase):
    _parser = ArgumentParser(
        description="Choose random words from dictionary.",
        usage="""xylophone -s structure --obj OBJECTIVES --adj ADJECTIVES --verb VERBS
               [--forced_obj FORCED_OBJECTIVES]
               [--foced_adj FORCED_ADJECTIVES] [--foced_verb FORCED_VERBS]
               [--sub_sentence_count SUB_SENTENCE_COUNT]
               [--sentence_count SENTENCE_COUNT] [--seed SEED]""",
        add_help=False)

    _parser.add_argument("--obj", dest="objects", required=True)
    _parser.add_argument("--adj", dest="adjectives", required=True)
    _parser.add_argument("--verb", dest="verbs", required=True)

    _parser.add_argument("--forced_obj", "-o", dest="forced_objects", default="")
    _parser.add_argument("--dots", default=".,,,,--::!?")

    _parser.add_argument("--each_parts_count", default=3, type=int)
    _parser.add_argument("--seed", dest="seed", default=None, type=int, help="PRNG seed.")

    def __init__(self, *args):
        self._args, self._unknown_args = self._parser.parse_known_args(args)

        self._random = random.Random(self._args.seed)
        self._each_parts_count = self._args.each_parts_count

        self._forced_objects = self._args.forced_objects.split(' ')

        self._dots = self._args.dots
        self._obj = self.shuffled(self._args.objects.split(' '))
        self._adj = self.shuffled(self._args.adjectives.split(' '))
        self._verb = self.shuffled(self._args.verbs.split(' '))

    def process(self) -> [str]:
        sentence = []

        for i in range(self._each_parts_count):
            sentence.append(self._obj[i])
            sentence.append(self._adj[i])
            sentence.append(self._verb[i])

        for i in range(math.ceil(self._each_parts_count / 2)):
            sentence.append(self._dots[i])

        sentence.extend(self._forced_objects)

        return [*self._unknown_args, ' '.join(self.shuffled(sentence))]

    def shuffled(self, arr):
        self._random.shuffle(arr)
        return arr

    @staticmethod
    def help() -> str:
        return Randomize._parser.format_help()
