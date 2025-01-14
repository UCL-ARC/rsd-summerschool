# ---
# jupyter:
#   jekyll:
#     display_name: Data Classes and Validation
#   jupytext:
#     notebook_metadata_filter: -kernelspec,jupytext,jekyll
#     text_representation:
#       extension: .py
#       format_name: percent
#       format_version: '1.3'
#       jupytext_version: 1.15.2
# ---

# %% [markdown]
# # Data Classes and Validation
# 
# ## Data Classes
# 
# ### dataclasses
# 
# Python 3.7 introduced the [@dataclass](https://docs.python.org/3/library/dataclasses.html) decorator to write
# classes meant to hold data with ease and minimal repetition. Consider the following
# example from our last chapter.


# %%
class Person:
    def __init__(self, birthday, name):
        self.birth_day = birthday[0]
        self.birth_month = birthday[1]
        self.birth_year = birthday[2]
        self.name = name

# %% [markdown]
# A good practice here would be to add other dunder methods like `__repr__` and `__eq__`
# for a better user experience. Let's do that.

# %%
class Person:
    def __init__(self, birth_day, birth_month, birth_year, name):
        self.birth_day = birth_day[0]
        self.birth_month = birth_month[1]
        self.birth_year = birth_year[2]
        self.name = name
    def __repr__(self):
        return f"Person(birth_day={self.birth_day}, birth_month={self.birth_month}, birth_year={self.birth_year}, name='{self.name}')"
    def __eq__(self, other):
        return (
            self.birth_day == other.birth_day
            and self.birth_month == other.birth_month
            and self.birth_year == other.birth_year
            and self.name == other.name
        )

# %% [markdown]
# Simple enough! But can we make it even simpler and DRYer? Yes!
# The `@dataclass` decorator automates the creation of a the `__init__`,
# `__repr__`, and `__eq__` methods.

# %%
from dataclasses import dataclass

@dataclass
class Person:
    birth_day: int
    birth_month: int
    birth_year: int
    name: str

# %% [markdown]
# That's it! Data classes rely heavily on static types. Let us try creating the objects and using the methods.

# %%
p1 = Person(7, 1, 2002, "Saransh")

# %%
p2 = Person(16, 3, 2002, "Hnin")

# %%
p1, p2

# %%
p1 == p2

# %%
p2 == p2

# %% [markdown]
# As regular classes, one can assign default values to the parameters.

# %%
@dataclass
class Person:
    birth_day: int = 1
    birth_month: int = 1
    birth_year: int = 1972
    name: str = "John Doe"

# %% [markdown]
# To have more flexibility, one can use the `field` function and pass in arguments
# such as `default` (default value), `repr` (whether to include in repr),
# `init` (whether to include in init), `compare` (whether to include in eq), etc.

# %%
from dataclasses import field

@dataclass
class Person:
    birth_day: int = field(default=1)
    birth_month: int = field(default=1)
    birth_year: int = field(default=1972)
    name: str = field(default="John Doe")

# %% [markdown]
# We can extend out example to include a `People` class that takes in a `list`
# of `Person`s and has the same basic dunder methods.

# %%
from typing import List

@dataclass
class People:
   person: List[Person] = []

# %% [markdown]
# Why does that throw an error? Using mutable objects as function argument defaults
# is a bad practice as they will be edited in-place inside the function definition.
# The argument variable is shared throughout all the calls to a function, which
# is known as ["call by sharing."](https://en.wikipedia.org/wiki/Evaluation_strategy)

# %%
def append_to_list(el, lst=[]):
    lst.append(el)
    return lst

# %%
append_to_list(0)

# %%
append_to_list(1)

# %% [markdown]
# The error can be fixed by using the `default_factory` parameter
# of the `fields` function.

# %%
@dataclass
class People:
   person: List[Person] = field(default_factory=list)

People([p1, p2])

# %% [markdown]
# Finally, dataclasses offer several other features to the users, such as -
# - ability to override the generated dunder methods
# - a `__post_init__` method for data validation
# - numerous arguments for the decorator -
#   - order: generate methods for comparison operators
#   - frozen: add no setter for the fields
#   - ...
# 
# Moreover, data classes are syntactic sugars to make your life easier when
# building classes that store data. They might not be very useful if you
# want the dunder methods to behave in a specific way, as you will end up
# overriding the generated methods. Additionally, given the `dataclasses`
# is part of the Python standard library, addition of new features and bug
# fixes are relatively slow, but it blends really well with Python and the
# fundamental PyData libraries. [attrs](https://www.attrs.org/en/stable/)
# is a third-party solution that allows one to write concise classes without
# much repetition.
# 
# ## Data Validation
# 
# Any kind of data requires proper validation before it can be used to execute
# actual science. Data validation allows your data pipelines to "fail fast" or
# fail at the very first step, saving compute resources and time. One can either
# define custom rules in `__init__` or `__post_init__`, or use libraries
# like pydantic to automate the process.
# 
# ### Pydantic
# 
# [Pydantic](https://docs.pydantic.dev/latest/) enables data validation using Python
# type hints and class inheritance.

# %%
from pydantic import BaseModel, Field

class Person(BaseModel):
    birth_day: int = Field(1)
    birth_month: int = Field(1)
    birth_year: int = Field(1972)
    name: str = Field("John Doe")

# %% [markdown]
# BaseModel subclasses take keyword arguments only. The `Field` class offers
# several powerful arguments, like -
# - examples: example values for the field
# - description: desription of the field
# - frozen: removes setters for the fields
# - init, repr, and compare as dataclass
# - ....

# %%
data = {"birth_day": 7, "birth_month": 1, "birth_year": 2002, "name": "Saransh"}
Person(**data)

# %% [markdown]
# Works like a data class!

# %%
p1 = Person(**{"birth_day": 7, "birth_month": 1, "birth_year": 2002, "name": "Saransh"})
p2 = Person(**{"birth_day": 16, "birth_month": 3, "birth_year": 2002, "name": "Hnin"})

p1, p2

# %%
p1 == p2

# %%
p1 == p1

# %% [markdown]
# But it can validate data using type hints.

# %%
Person.model_validate(data)

# %%
bad_data = {"birth_day": 7, "birth_month": 1, "birth_year": 2002, "name": 1}

Person.model_validate(bad_data)

# %% [markdown]
# The library further offers custom types, such as `EmailStr` for email address
# validation or `SecretStr` which hides sensitive information. Users can also
# write their own validation scripts using the `@field_validator` decorator.

# %%
from pydantic import field_validator

class Person(BaseModel):
    birth_day: int = Field(1)
    birth_month: int = Field(1)
    birth_year: int = Field(1972)
    name: str = Field("John Doe")
    
    @field_validator("name")
    @classmethod
    def validate_name(cls, v: str) -> str:
        if " " not in v:
            raise ValueError("the name must have first and last names separated by <space>")
        return v

# %% [markdown]
# Similarly, the whole data model or connect multiple fields together for
# validation using `@model_validator`. The "after" mode tell pydantic to run
# its own validations on the data before running the custom validations
# defined by the user.

# %%
from pydantic import model_validator
from typing import Any

class Person(BaseModel):
    birth_day: int = Field(1)
    birth_month: int = Field(1)
    birth_year: int = Field(1972)
    name: str = Field("John Doe")
    
    @model_validator(mode="after")
    @classmethod
    def validate_name(self, v: Any) -> Person:
        if " " not in v["name"]:
            raise ValueError("the name must have first and last names separated by <space>")
        if v["birth_month"] < 1 or v["birth_month"] > 12:
            raise ValueError("birth month should be between 1 and 12")
        if v["birth_month"] in [1, 3, 5, 7, 8, 10, 12] and (v["birth_day"] < 1 or v["birth_day"] > 31):
            raise ValueError("birth day should be between 1 and 31")
        if v["birth_month"] in [4, 6, 9, 11] and (v["birth_day"] < 1 or v["birth_day"] > 31):
            raise ValueError("birth day should be between 1 and 30")
        if v["birth_month"] == 2:
            if (v["birth_year"] % 400 == 0 or v["birth_year"] % 4 == 0):
                if v["birth_day"] < 1 or v["birth_day"] > 29:
                    raise ValueError("birth day should be between 1 and 29")
            else:
                    raise ValueError("birth day should be between 1 and 28")
        return v

# %% [markdown]
# Pydantic has a ton of other features and functionalities that make data processing
# for every domain easy and simple. Overall, static typing facilitates data classes
# and pydantic validations. Several libraries build on top of pydantic to provide
# domain specific validation tools. For example [BPX](https://github.com/FaradayInstitution/BPX)
# implements the Battery Parameter eXchange (BPX) schema in Pydantic with validation
# parsing, and JSON serialization capabilities.
