import argparse

from xylophone import resources
from xylophone.stages.base import StageBase, register_stage


@register_stage("words-dict")
class WordsDict(StageBase):
    _parser = argparse.ArgumentParser(
        usage="xylophone -s words-dict [--obj-add OBJECTS_ADDITIONAL] [--adj-add ADJECTIVES_ADDITIONAL] "
              "[--verb-add VERBS_ADDITIONAL] [--obj_source OBJECTS_SOURCE] [--adj_source ADJECTIVES_SOURCE] "
              "[--verb_source VERBS_SOURCE]",
        description="Words dictionary source.",
        add_help=False)

    _parser.add_argument("--obj-add", '-o', dest="objects_additional", default="")
    _parser.add_argument("--adj-add", '-a', dest="adjectives_additional", default="")
    _parser.add_argument("--verb-add", '-v', dest="verbs_additional", default="")

    _parser.add_argument("--obj_source", dest="objects_source", default="default/objects.txt")
    _parser.add_argument("--adj_source", dest="adjectives_source", default="default/adjectives.txt")
    _parser.add_argument("--verb_source", dest="verbs_source", default="default/verbs.txt")

    def __init__(self, *args: [str]):
        self._args, self._unknown_args = self._parser.parse_known_args(args)

    def process(self) -> [str]:
        objects = resources.read(self._args.objects_source) + " " + self._args.objects_additional
        adjectives = resources.read(self._args.adjectives_source) + " " + self._args.adjectives_additional
        verbs = resources.read(self._args.verbs_source) + " " + self._args.verbs_additional
        return [*self._unknown_args, "--obj", objects, "--adj", adjectives, "--verb", verbs]

    @staticmethod
    def help() -> str:
        return WordsDict._parser.format_help()
