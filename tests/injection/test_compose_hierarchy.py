from injector import *


class Greeter:
    def greet(self, name):
        pass

class PoliteGreeter(Greeter):
    def greet(self, name):
        return f"Hello, {name}."

class Program():
    @inject
    def __init__(self, greeter:Greeter):
        self.greeter = greeter

    def run(self):
        print(self.greeter.greet('Lars-Erik'))

def configure_dependencies(binder: Binder):
    binder.bind(Greeter, to=PoliteGreeter)
    binder.bind(Program)

def test_composed_hierarchy(capsys):
    injector = Injector([configure_dependencies])
    injector.get(Program).run()

    assert capsys.readouterr().out == 'Hello, Lars-Erik.\n'