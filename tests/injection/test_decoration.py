from datetime import datetime
from pprint import pprint

from injector import *

class BaseGreeter:
    def greet(self, name) -> str:
        pass

class Greeter(BaseGreeter):
    def greet(self, name):
        return f"Hi, {name}"

class SomeDependency:
    pass

class TimeGreeter(BaseGreeter):
    def __init__(self, inner: BaseGreeter, dep: SomeDependency):
        self.inner = inner

    def greet(self, name):
        result = self.inner.greet(name)
        result = result + ". Lovely " + ("afternoon" if datetime.now().hour > 12 else "morning")
        return result

@inject
def create_greeter(dep: SomeDependency):
    return TimeGreeter(Greeter(), dep)

def configure(binder: Binder):
    binder.bind(SomeDependency)
    binder.bind(BaseGreeter, to=create_greeter)

def test_decoration():
    container = Injector([configure])
    greeter = container.get(BaseGreeter)
    result = greeter.greet('Lars-Erik')
    pprint('\n')
    pprint(result)
    assert result in [
        "Hi, Lars-Erik. Lovely afternoon",
        "Hi, Lars-Erik. Lovely morning"
    ]

