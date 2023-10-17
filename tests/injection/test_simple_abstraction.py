from injector import *


class Greeter:
    def greet(self, name):
        pass

class PoliteGreeter(Greeter):
    def greet(self, name):
        return f"Hello, {name}."

def configure_dependencies(binder: Binder):
    binder.bind(Greeter, to=PoliteGreeter)

def test_simple_abstraction():
    container = Injector([configure_dependencies])
    greeter = container.get(Greeter)

    result = greeter.greet('Lars-Erik')

    print(f'\n{result}')
    assert result == 'Hello, Lars-Erik.'

