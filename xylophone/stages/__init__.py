import shlex

from .base import StageBase, STAGES

from .structure import Structure
from .translate import Translate
from .words_dict import WordsDict


class InvalidStageCmdException(Exception):
    def __init__(self, stage_cmd):
        self.stage_cmd = stage_cmd


class StageNotExistsException(Exception):
    def __init__(self, stage_name):
        self.stage_name = stage_name


def run_xylophone(pipe_cmd: str, args: list[str]) -> [str]:
    for stage_cmd in pipe_cmd.split('|'):
        args = invoke_stage(stage_cmd, args)
    return args


def invoke_stage(stage_cmd: str, args: list[str]) -> [str]:
    stage = create_stage(stage_cmd, args)

    return stage.process()


def create_stage(stage_cmd, args: list[str]):
    stage_args = shlex.split(stage_cmd)

    if len(stage_args) == 0:
        raise InvalidStageCmdException(stage_cmd)

    stage_name = stage_args[0]
    if stage_name not in STAGES:
        raise StageNotExistsException(stage_name)

    if len(stage_args) > 1:
        args.extend(stage_args[1:])

    stage_cls = STAGES[stage_name]
    stage: StageBase = stage_cls(*args)

    return stage


def get_stage_help(stage_name) -> str:
    if stage_name not in STAGES:
        raise StageNotExistsException(stage_name)
    return STAGES[stage_name].help()


def stage_exists(stage_name) -> bool:
    return stage_name in STAGES
