from typing import Protocol

class BaseClass(Protocol):
    def __len__(self) -> int: ...


class A:
    def __len__(self) -> int:
        return 5

class B:
    def __len__(self) -> int:
        return 6


def f(el: BaseClass) -> None:
    print(len(el))


a = A()
b = B()

f(a)
f(b)
f({1: 1, 2: 2})
f([1, 2])
