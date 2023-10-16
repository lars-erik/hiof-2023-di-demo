from pprint import pprint

import injector
from typing import TypeVar, Generic

class Command:
    pass

TCommand = TypeVar('TCommand', bound=Command)

class Handler(Generic[TCommand]):
    __args__ = [TCommand]
    def execute(self, cmd: TCommand):
        pass

class CommandA(Command):
    def __init__(self, message):
        self.message = message

class CommandB(Command):
    def __init__(self, signal):
        self.signal = signal

class AHandler(Handler[CommandA]):
    __args__ = [CommandA]
    def execute(self, cmd: CommandA):
        return f"I got a message: {cmd.message}"

class BHandler(Handler[CommandB]):
    __args__ = [CommandB]
    def execute(self, cmd: CommandB):
        return f"I got a signal: {cmd.signal}"

def configure(binder):
    binder.bind(Handler[CommandA], to=AHandler)
    binder.bind(Handler[CommandB], to=BHandler)

def test_handler_factory():
    container = injector.Injector([configure])

    verify_commands(container)


def autodiscover(binder):
    for subclass in Handler.__subclasses__():
        if hasattr(subclass, '__args__') and subclass.__args__[0] in Command.__subclasses__():
            binder.bind(Handler[subclass.__args__[0]], to=subclass)


def test_autodiscovery():
    container = injector.Injector([autodiscover])

    verify_commands(container)

def verify_commands(container):
    result = execute(CommandA("A message"), container)
    assert result == "I got a message: A message"
    result = execute(CommandB("A signal"), container)
    assert result == "I got a signal: A signal"

def execute(cmd, container):
    handler = container.get(Handler[type(cmd)])
    result = handler.execute(cmd)
    return result
