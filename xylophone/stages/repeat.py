from .base import StageBase, ArgumentParser, register_stage, invoke_stage


@register_stage("repeat")
class Repeat(StageBase):
    _parser = ArgumentParser(description="Repeat stage and concat results",
                             usage="xylophone -s repeat --cmd CMD [--count COUNT] [--separator SEPARATOR]",
                             add_help=False)
    
    _parser.add_argument("--cmd", required=True)
    _parser.add_argument("--count", "-c", type=int, default=1)
    _parser.add_argument("--separator", "-s", default="\n")

    def __init__(self, *args):
        self._args, self._unknown_args = self._parser.parse_known_args(args)

    def process(self) -> [str]:
        output = [invoke_stage(self._args.cmd, self._unknown_args)[0] for _ in range(self._args.count)]
        return [self._args.separator.join(output)]

    @staticmethod
    def help() -> str:
        return Repeat._parser.format_help()
