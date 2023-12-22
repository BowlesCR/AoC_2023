from __future__ import annotations
import fileinput
import re
from abc import ABC, abstractmethod
from collections import deque


class Module(ABC):
    queue: deque[tuple[Module, tuple[Module, bool]]] = deque()

    def __init__(self, name: str):
        self.name = name
        self.outputs: list[Module] = []

    @abstractmethod
    def input(self, caller: Module, high: bool) -> None:
        pass

    def _output(self, high: bool) -> None:
        for dest in self.outputs:
            Module.queue.append((dest, (self, high)))


class FlipFlop(Module):
    def __init__(self, name: str):
        super().__init__(name)
        self.state_high: bool = False

    def input(self, caller: Module, high: bool) -> None:
        if high:
            return

        self.state_high ^= True
        self._output(self.state_high)


class Conjunction(Module):
    def __init__(self, name: str):
        super().__init__(name)
        self.inputs: dict[str, bool] = {}

    def input(self, caller: Module, high: bool) -> None:
        self.inputs[caller.name] = high

        self._output(not all(self.inputs.values()))


class Broadcaster(Module):
    def __init__(self, name: str):
        super().__init__(name)

    def input(self, caller: Module, high: bool) -> None:
        self._output(high)


class Dummy(Module):
    def __init__(self, name: str):
        super().__init__(name)

    def input(self, caller: Module, high: bool) -> None:
        return


def main():
    re_line = re.compile(r"^([%&])?(\w+) -> (.+)$")

    config: dict[str, tuple[Module, list[str]]] = {}
    for line in fileinput.input():
        m = re_line.match(line)
        modtype, name, dests = m.groups()
        dests = dests.split(", ")
        if name == "broadcaster":
            config[name] = (Broadcaster(name), dests)
        elif modtype == "%":
            config[name] = (FlipFlop(name), dests)
        elif modtype == "&":
            config[name] = (Conjunction(name), dests)
        else:
            assert False
    del m, modtype, name, dests

    for m in config.values():
        for d in m[1]:
            if d in config:
                dest: Module = config[d][0]
            else:
                print(d)
                dest = Dummy(d)
            m[0].outputs.append(dest)
            if type(dest) is Conjunction:
                dest: Conjunction
                dest.inputs[m[0].name] = False
    del m, d, dest

    broadcaster = config["broadcaster"][0]
    del config

    high = 0
    low = 0
    for _ in range(1000):
        broadcaster.input(None, False)
        low += 1

        while Module.queue:
            pulse = Module.queue.popleft()
            pulse[0].input(*pulse[1])
            if pulse[1][1]:
                high += 1
            else:
                low += 1

    print(high * low)


if __name__ == "__main__":
    main()
