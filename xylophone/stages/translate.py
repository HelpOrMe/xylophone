from deep_translator import GoogleTranslator
from .base import StageBase, ArgumentParser, register_stage


@register_stage("translate")
class Translate(StageBase):
    _parser = ArgumentParser(
        usage="xylophone -s translate [--from SOURCE] --to TARGET text",
        description="Text translator.",
        add_help=False)

    _parser.add_argument("text", help="Text to translate")
    _parser.add_argument("--from", dest="source", default="auto", help="From language")
    _parser.add_argument("--to", dest="target", required=True, help="To language")

    def __init__(self, *args):
        self._args, self._unknown_args = self._parser.parse_known_args(args)
        self._translator = GoogleTranslator(source=self._args.source, target=self._args.target)

    def process(self) -> [str]:
        return [*self._unknown_args, self._translator.translate(self._args.text)]

    @staticmethod
    def help() -> str:
        return Translate._parser.format_help()
