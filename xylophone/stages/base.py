import shlex
import argparse
import abc

STAGES: dict[str, any] = {}


class XylophoneStageException(Exception):
    def __init__(self, message):
        self.message = message


class ArgumentParser(argparse.ArgumentParser):
    def error(self, message: str):
        raise XylophoneStageException(message)


class StageBase(abc.ABC):
    @abc.abstractmethod
    def __init__(self, *args: [str]):
        pass

    @abc.abstractmethod
    def process(self) -> [str]:
        pass

    @staticmethod
    @abc.abstractmethod
    def help() -> str:
        pass


def register_stage(name):
    def wrapper(cls):
        STAGES[name] = cls
        return cls
    return wrapper


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


def create_stage(stage_cmd, args: list[str]) -> StageBase:
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
