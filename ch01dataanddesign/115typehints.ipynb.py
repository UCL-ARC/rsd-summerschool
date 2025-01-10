# ---
# jupyter:
#   jekyll:
#     display_name: Static Typing
#   jupytext:
#     notebook_metadata_filter: -kernelspec,jupytext,jekyll
#     text_representation:
#       extension: .py
#       format_name: percent
#       format_version: '1.3'
#       jupytext_version: 1.15.2
# ---

# %% [markdown]
# # Static Typing
# 
# Python is a dynamically types and interpreted language, but over the years
# Python community has developed tools and frameworks to add (non-strict) type
# hints to Python code.
# 
# These type hints, even though not strict, offer users a much clear picture
# of how the code is supposed to be used. Besides offering help to the users,
# type hints also improve documentation, as the leading static site generators
# can pick type hints from your code and render them in the documentation
# automatically.
# 
# In addition to the UX improvements, type hints often help developers catch
# silent bugs, dead code, or missing functionalities in downstream code. Further
# libraries like [mypyc](https://mypyc.readthedocs.io/en/latest/introduction.html)
# can compile Python modules to C extensions by simply using the type hints added
# by developers, offering a speedup in your standard Python code.
# 
# ## Looking at types
# 
# Let's see how types can be defined for Python variables and function signatures.

# %%
a: int = 5  # a is of type int

# %%
def add(a: int, b: int) -> int:  # takes in 2 `int`s and returns an `int`
    return a + b

# %%
def hello(name: str) -> None:  # takes in a `str` and return `None`
    print("hello", name)
    
# But are these types rigid?

# %%
type(a)  # declared `int` above

# %%
a = 5.5

# %%
type(a)

# %% [markdown]
# No! In fact, the typing information printed by `type()` is not
# gathered through the type hint, instead, it uses the type assigned
# to the variable dynamically by Python interpretor. So how does the
# the typing information help us?
# 
# ## Static type checkers
# 
# Static type checkers can be used to verify if the codebase is adhering
# to the type hints declared by the developers. There are a number of
# tools and frameworks available for checking type information in the
# Python ecosystem:
# 
# * [mypy](https://mypy.readthedocs.io/en/stable/): a static type checker for Python
# * [pytype](https://google.github.io/pytype/): checks and infers types for Python code - without requiring type annotations
# * [pyright](https://microsoft.github.io/pyright/): a full-featured, standards-compliant static type checker for Python
# * [pyre](https://pyre-check.org): a performant type-checker for Python 3
# 
# Mypy is one of the oldest open-sourced and the most widely used static type
# checker for Python code. The tool is also recommended by Scientific Python,
# so our examples below will use mypy, but feel free to experiment with the
# other tools as well. Additionally, most of the IDEs either provide integration
# support for the static typing tools listed above or offer their own solutions for
# checking static types.
# 
# ## Mypy
# 
# We can write the same code in a file and run mypy over it to check the
# correctness of types:

# %% jupyter={"outputs_hidden": false}
# %%writefile static_types_example.py
a: int = 5
a = 5.5

# %% attributes={"classes": [" Bash"], "id": ""} jupyter={"outputs_hidden": false} language="bash"
mypy static_types_example.py

# %% [markdown]
# Mypy correctly points out that we are reassigning `a` to a floating point
# number, but it was declared as an integer on line 1. How about function
# calls?

# %% jupyter={"outputs_hidden": false}
# %%writefile static_types_example.py
def add(a: int, b: int) -> int:
    return a + b

def hello(name: str) -> None:
    print("hello", name)

add(1, 2)
hello("Saransh")
add(1.5, 2)
hello(5)

# %% attributes={"classes": [" Bash"], "id": ""} jupyter={"outputs_hidden": false} language="bash"
mypy static_types_example.py

# %% [markdown]
# Mypy correctly points out that we are using the functions wrong!
# 
# Mypy includes the functions `reveal_type()` and `reveal_locals()`
# to check the type of variables programatically on run time. These
# functions should not be used when running your modules through the
# Python interpretor, but they can be used when you are running mypy
# over your modules.

# %% jupyter={"outputs_hidden": false}
# %%writefile static_types_example.py
def add(a: int, b: int) -> int:
    return a + b

def hello(name: str) -> None:
    print("hello", name)

a = add(1, 2)
reveal_type(a)

b = hello("Saransh")
reveal_type(b)

c = 5
reveal_locals()

# %% attributes={"classes": [" Bash"], "id": ""} jupyter={"outputs_hidden": false} language="bash"
mypy static_types_example.py

# %% [markdown]
# ## typing, types, and collections
# 
# The [`typing`](https://docs.python.org/3/library/typing.html)
# module of Python offers the building blocks for type annotations, such as
# `Any` and `Never`, advanced features, such as `Protocol`, `TypeVar`,
# `NewType`, `Generic` and `TypeAlias`, and useful functions, such as
# `reveal_type()`.
# 
# Similarly, the [`types`](https://docs.python.org/3/library/types.html)
# module offers additional built-in types, such as the `NoneType`,
# `LambdaType`, and `ModuleType`. Besides `typing` and `types`, the
# [`collections.abc`](https://docs.python.org/3/library/collections.abc.html)
# offers abstract base classes for data containers, such as `Sequence`,
# `Iterable`, `Mapping`, and `Set`.
# 
# Let's code up a dummy calculator class to see some of the typing annotations
# in action.

# %% jupyter={"outputs_hidden": false}
# %%writefile static_types_example.py
class Calculator:
    def __init__(self, a):
        self.a = a
    def add(self, b):
        return self.a + b
    def add_multi(self, *b):
        return sum((self.a, *b))
    def subtract(self, b):
        return self.a - b
    def multiply(self, b):
        return self.a * b
    def divide(self, b, check_zero=True):
        if check_zero and b == 0:
            return None
        return self.a / b
    def transform(self, tfm):
        return tfm(self.a)
    def idx(self, sqnc):
        if isinstance(a, float):
            raise ValueError("a should be int")
        try:
            rslt = sqnc[a]
        except IndexError:
            raise ValueError("sequence too small")
        return rslt

# %% [markdown]
# The class can be updated with basic typing information.

# %% jupyter={"outputs_hidden": false}
# %%writefile static_types_example.py
from collections.abc import Callable
from typing import Union, Optional, Any

class Calculator:
    def __init__(self, a: Union[int, float]) -> None:
        self.a = a
    def add(self, b: Union[int, float]) -> Union[int, float]:
        return self.a + b
    # *args and **kwargs need type annotation for what each argument
    # can be
    def add_multi(self, *b: Union[int, float]) -> Union[int, float]:
        return sum((self.a, *b))
    def subtract(self, b: Union[int, float]) -> Union[int, float]:
        return self.a - b
    def multiply(self, b: Union[int, float]) -> Union[int, float]:
        return self.a * b
    def divide(self, b: Union[int, float], check_zero: Optional[bool] = True) -> Optional[Union[int, float]]:
        if check_zero and b == 0:
            return None
        return self.a / b
    # tfm is a function (`Callable`) that takes an `int` or `float`
    # as an argument and can output anything (`Any`)
    def transform(self, tfm: Callable[[Union[int, float]], Any]):
        return tfm(self.a)
    def idx(self, sqnc):
        if isinstance(a, float):
            raise ValueError("a should be int")
        try:
            rslt = sqnc[a]
        except IndexError:
            raise ValueError("sequence too small")
        return rslt

# %% attributes={"classes": [" Bash"], "id": ""} jupyter={"outputs_hidden": false} language="bash"
mypy static_types_example.py

# %% [markdown]
# Notice how mypy does not error out on missing types for `transform()`.
# This is because mypy supports
# [gradual typing](https://wphomes.soic.indiana.edu/jsiek/what-is-gradual-typing/).
# 
# We can update the type hints to be more modern:

# %% jupyter={"outputs_hidden": false}
# %%writefile static_types_example.py
from typing import Any
from collections.abc import Callable

class Calculator:
    def __init__(self, a: int | float) -> None:
        self.a = a
    def add(self, b: int | float) -> int | float:
        return self.a + b
    def add_multi(self, *b: int | float) -> int | float:
        return sum((self.a, *b))
    def subtract(self, b: int | float) -> int | float:
        return self.a - b
    def multiply(self, b: int | float) -> int | float:
        return self.a * b
    def divide(self, b: int | float, check_zero: bool | None = True) -> int | float | None:
        if check_zero and b == 0:
            return None
        return self.a / b
    def transform(self, tfm: Callable[[int | float], Any]):
        return tfm(self.a)
    def idx(self, sqnc):
        if isinstance(a, float):
            raise ValueError("a should be int")
        try:
            rslt = sqnc[a]
        except IndexError:
            raise ValueError("sequence too small")
        return rslt

# %% [markdown]
# ## Type aliases and generic types
# 
# Or dig into some advanced concepts like `TypeAlias` and `TypeVar`.

# %% jupyter={"outputs_hidden": false}
# %%writefile static_types_example.py
from typing import TypeAlias, Union, TypeVar, Any
from collections.abc import Sequence, Callable

number: TypeAlias = Union[int, float]
# or just
# number = int | float
T = TypeVar("T")

class Calculator:
    def __init__(self, a: number) -> None:
        self.a = a
    def add(self, b: number) -> number:
        return self.a + b
    def add_multi(self, *b: number) -> number:
        return sum((self.a, *b))
    def subtract(self, b: number) -> number:
        return self.a - b
    def multiply(self, b: number) -> number:
        return self.a * b
    def divide(self, b: number, check_zero: bool | None = True) -> number | None:
        if check_zero and b == 0:
            return None
        return self.a / b
    def transform(self, tfm: Callable[[number], Any]):
        return tfm(self.a)
    # takes a Sequence with each element of some type T, and returns
    # a variable of the type T
    def idx(self, sqnc: Sequence[T]) -> T:
        if isinstance(self.a, float):
            raise ValueError("a should be int")
        try:
            rslt = sqnc[self.a]
        except IndexError:
            raise ValueError("sequence too small")
        return rslt

# %% attributes={"classes": [" Bash"], "id": ""} jupyter={"outputs_hidden": false} language="bash"
mypy static_types_example.py

# %% [markdown]
# ## Duck Typing and Protocols
# 
# Duck Typing is often referred to as "If it walks like a duck and it quacks like a duck, then it must be a duck."
# Languages like Python can treat a variable of a given type if it implements all the methods
# properties implemented/required by the type.
# 
# For instance, the `len` method can be called in a similar manner on the built-in list
# type, or on out custom class:

# %%
class Container:
    def __len__(self):
        return 5

# %%
c = Container()
len(c)

# %% [markdown]
# A good example of duck typing is how one can use same standard library
# functions on tuples, lists, strings, sets, and dictionaries without
# explicitly telling the function the type of the argument.

# %%
lst = [1, 2, 3]
tpl = (1, 2, 3)
st = {1, 2, 3}
strng = "123"
dct = {1: 1, 2: 2, 3: 3}

# %%
sorted(lst, reverse=True)

# %%
sorted(tpl, reverse=True)

# %%
sorted(st, reverse=True)

# %%
sorted(strng, reverse=True)

# %%
sorted(dct, reverse=True)

# %% [markdown]
# Thanks to duck typing, one usually does not need to deal with
# [Abstract Base Classes](https://docs.python.org/3/library/abc.html) or
# [Interfaces](https://en.wikipedia.org/wiki/Interface_(object-oriented_programming))
# in Python, but a [Protocols](https://typing.readthedocs.io/en/latest/spec/protocol.html)
# are often useful for subtyping Python classes.
#
# Protocols allow multiple classes to act as the same type if they
# implement the same methods or "protocol members". Let's construct a
# Protocol subclass and 2 other classes with the same method.

# %% jupyter={"outputs_hidden": false}
# %%writefile static_types_example.py
from typing import Protocol

class BaseClass(Protocol):
    def __len__(self) -> int: ...


class A:
    def __len__(self) -> int:
        return 5

class B:
    def __len__(self) -> int:
        return 6

# %% [markdown]
# We can then define a function that takes an argument of type
# `BaseClass` and prints its length. Let's call it on a bunch
# of arguments.

# %% jupyter={"outputs_hidden": false}
# %%writefile static_types_example.py
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

# %% attributes={"classes": [" Bash"], "id": ""} jupyter={"outputs_hidden": false} language="bash"
mypy static_types_example.py

# %% [markdown]
# mypy does not error out! This is because `A` and `B` are "structural"
# subtypes of `BaseClass` or is an "implementation" of the Protocol.
# 
# Do you think the function will accept aa dictionary or a list as an input
# without mypy complaining?

# %% jupyter={"outputs_hidden": false}
# %%writefile static_types_example.py
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

# %% attributes={"classes": [" Bash"], "id": ""} jupyter={"outputs_hidden": false} language="bash"
mypy static_types_example.py

# %% [markdown]
# Yes, it does! Technically, `dict` and `list` are also implementations
# of our Protocol as they include a `__len__()` method.
# 
# Static typing is a very powerful tool to have in your arsenal while
# writing Python code. In the next few chapters, we will see how static
# types can help us make better design choices (we saw some of it above)
# and even test our code to detect things like silent bugs or dead
# lines.
# 
# Further reading:
# - Introduction to type systems: https://adabeat.com/fp/introduction-to-type-systems/
# - Type hints cheat sheet: https://mypy.readthedocs.io/en/stable/cheat_sheet_py3.html
# - PEP 484 – Type Hints: https://peps.python.org/pep-0484/
# 