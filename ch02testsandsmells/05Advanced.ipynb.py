# ---
# jupyter:
#   jekyll:
#     display_name: Advanced Testing Techniques
#   jupytext:
#     notebook_metadata_filter: -kernelspec,jupytext,jekyll
#     text_representation:
#       extension: .py
#       format_name: percent
#       format_version: '1.3'
#       jupytext_version: 1.15.2
# ---

# %% [markdown]
# # Advanced Testing Techniques
# 
# Unit and integration tests are great, but they are often not enough for
# large and complex codebases. There are several other advanced testing techniques
# that are being adopted as a new standard throughout organisations. We
# discuss a few of them below.
# 
# ## Mocking
#
# **Mock**: *verb*,
#
# 1. to tease or laugh at in a scornful or contemptuous manner
# 2. to make a replica or imitation of something
#
# **Mocking**
#
# Replace a real object with a pretend object, which records how it is called, and can assert if it is called wrong
# 
# ### Mocking frameworks
#
# * C: [CMocka](http://www.cmocka.org/)
# * C++: [googletest](https://github.com/google/googletest)
# * Python: [unittest.mock](http://docs.python.org/3/library/unittest.mock)
# 
# ### Recording calls with mock
#
# Mock objects record the calls made to them:

# %%
from unittest.mock import Mock
function = Mock(name="myroutine", return_value=2)

# %%
function(1)

# %%
function(5, "hello", a=True)

# %% attributes={"classes": [" python"], "id": ""}
function.mock_calls

# %% [markdown]
# The arguments of each call can be recovered

# %% attributes={"classes": [" python"], "id": ""}
name, args, kwargs = function.mock_calls[1]
args, kwargs

# %% [markdown]
# Mock objects can return different values for each call

# %%
function = Mock(name="myroutine", side_effect=[2, "xyz"])

# %%
function(1)

# %%
function(1, "hello", {'a': True})

# %% [markdown]
# We expect an error if there are no return values left in the list:

# %%
function()

# %% [markdown]
# ## Using mocks to model test resources

# %% [markdown]
# Often we want to write tests for code which interacts with remote resources. (E.g. databases, the internet, or data files.)

# %% [markdown]
# We don't want to have our tests *actually* interact with the remote resource, as this would mean our tests failed
# due to lost internet connections, for example.

# %% [markdown]
# Instead, we can use mocks to assert that our code does the right thing in terms of the *messages it sends*: the parameters of the
# function calls it makes to the remote resource.

# %% [markdown]
# For example, consider the following code that downloads a map from the internet:

# %%
# sending requests to the web is not fully supported on jupyterlite yet, and the
# cells below might error out on the browser (jupyterlite) version of this notebook
import requests

def map_at(lat, long, satellite=False, zoom=12, 
           size=(400, 400)):

    base = "https://static-maps.yandex.ru/1.x/?"
    
    params = dict(
        z = zoom,
        size = ",".join(map(str,size)),
        ll = ",".join(map(str,(long,lat))),
        lang = "en_US")
    
    if satellite:
        params["l"] = "sat"
    else:
        params["l"] = "map"
        
    return requests.get(base, params=params)


# %%
london_map = map_at(51.5073509, -0.1277583)
from IPython.display import Image

# %%
# %matplotlib inline
Image(london_map.content)

# %% [markdown]
# We would like to test that it is building the parameters correctly. We can do this by **mocking** the requests object. We need to temporarily replace a method in the library with a mock. We can use "patch" to do this:

# %%
from unittest.mock import patch
with patch.object(requests,'get') as mock_get:
    london_map = map_at(51.5073509, -0.1277583)
    print(mock_get.mock_calls)


# %% [markdown]
# Our tests then look like:

# %%
def test_build_default_params():
    with patch.object(requests,'get') as mock_get:
        default_map = map_at(51.0, 0.0)
        mock_get.assert_called_with(
        "https://static-maps.yandex.ru/1.x/?",
        params={
            'z':12,
            'size':'400,400',
            'll':'0.0,51.0',
            'lang':'en_US',
            'l': 'map'
        }
    )
test_build_default_params()


# %% [markdown]
# That was quiet, so it passed. When I'm writing tests, I usually modify one of the expectations, to something 'wrong', just to check it's not
# passing "by accident", run the tests, then change it back!

# %% [markdown]
# ### Testing functions that call other functions
#
# <div align="left">

# %% attributes={"classes": [" python"], "id": ""}
def partial_derivative(function, at, direction, delta=1.0):
    f_x = function(at)
    x_plus_delta = at[:]
    x_plus_delta[direction] += delta
    f_x_plus_delta = function(x_plus_delta)
    return (f_x_plus_delta - f_x) / delta


# %% [markdown]
# We want to test that the above function does the right thing. It is supposed to compute the derivative of a function
# of a vector in a particular direction.

# %% [markdown]
# E.g.:

# %%
partial_derivative(sum, [0,0,0], 1)

# %% [markdown]
# How do we assert that it is doing the right thing? With tests like this:

# %%
from unittest.mock import MagicMock

def test_derivative_2d_y_direction():
    func = MagicMock()
    partial_derivative(func, [0,0], 1)
    func.assert_any_call([0, 1.0])
    func.assert_any_call([0, 0])
    

test_derivative_2d_y_direction()

# %% [markdown]
# We made our mock a "Magic Mock" because otherwise, the mock results `f_x_plus_delta` and `f_x` can't be subtracted:

# %%
MagicMock() - MagicMock()

# %%
Mock() - Mock()

# %% [markdown]
# ## Static type hints
# Although static type hints are not actual "tests," they can be checked under
# test runs (or CI pipelines) using static typing tools and libraries. Checking
# if the codebase is statically typed and the types are correct can help in
# finding silent bugs, dead code, and unreachable statements, which is often missed
# during unit and integration testing.
# 
# ### Static type checkers
# 
# * [mypy](https://mypy.readthedocs.io/en/stable/): a static type checker for Python
# * [pytype](https://google.github.io/pytype/): checks and infers types for Python code - without requiring type annotations
# * [pyright](https://microsoft.github.io/pyright/): a full-featured, standards-compliant static type checker for Python
# * [pyre](https://pyre-check.org): a performant type-checker for Python 3
# 
# Mypy is one of the oldest open-sourced and the most widely used static type
# checker for Python code. The tool is also recommended by Scientific Python,
# so our examples below will use mypy, but feel free to experiment with the
# other tools as well. Additionally, ,ost of the IDEs either provide integration
# support for the static typing tools listed above or offer their own solutions for
# checking static types.
# 
# ### Detecting dead code
# 
# For example, let's consider the following piece of code:

# %% jupyter={"outputs_hidden": false}
# %%writefile static_types_example.py
def smart_square(a: float | int | bool | str) -> int | float:
    if isinstance(a, (float, int)):
        return a * a
    elif isinstance(a, (str, bool)):
        try:
            result = float(a) * float(a)
            return result
        except ValueError:
            raise ValueError(f"a should be of type float/int or convertible to float; got {type(a)}")
    elif not isinstance(a, (float, int, bool, str)):
        raise NotImplementedError

# %% [markdown]
# The code looks good enough, squaring the argument if it is of type `float`
# or `int` and attempting to convert it to `float` if it is not. It looks like
# the code is clean, and testing it gives us no errors too -

# %% jupyter={"outputs_hidden": false}
# %%writefile test_static_types_example.py
import pytest
from static_types_example import smart_square

def test_smart_square():
    assert smart_square(2) == 4
    assert isinstance(smart_square(2), int)
    assert smart_square(2.) == 4.
    assert isinstance(smart_square(2.), float)
    assert smart_square("2") == 4.
    assert smart_square(True) == 1.

    with pytest.raises(ValueError, match="float/int or convertible to float; got <class 'str'>"):
        smart_square("false")

# %% attributes={"classes": [" Bash"], "id": ""} jupyter={"outputs_hidden": false} language="bash"
pytest test_static_types_example.py

# %% [markdown]
# Even though the tests look good, we can notice one peculiar
# behavior. We cannot test the `NotImplementedError` because it is not reachable,
# given that either the `if` or the `elif` condition will always be met
# and the argument type cannot be anything other than `float`, `int`, `bool`,
# or `str`; hence, the code will never go to the `else` statement.
# 
# This is called "unreachable" or "dead" code, and having it in your codebase
# is a bad practice. How do we detect it? Static types!
# 
# Let's run mypy with `--warn-unreachable` -

# %% attributes={"classes": [" Bash"], "id": ""} jupyter={"outputs_hidden": false} language="bash"
mypy static_types_example.py --warn-unreachable

# %% [markdown]
# The type checker points out that the line 9 (`else`) statement, is in fact
# unreachable. This could either be a bug - code that should be reachable
# but for some reason is not - or just dead code - code that will never
# be reached and can be removed. In out case it is dead code, and can be
# removed safely, given that we explicitly tell users what type of arguments should
# be passed in.

# %% jupyter={"outputs_hidden": false}
# %%writefile static_types_example.py
def smart_square(a: float | int | bool | str) -> int | float:
    if isinstance(a, (float, int)):
        return a * a
    elif isinstance(a, (str, bool)):
        try:
            result = float(a) * float(a)
            return result
        except ValueError:
            raise ValueError(f"a should be of type float/int or convertible to float; got {type(a)}")
    
# %% attributes={"classes": [" Bash"], "id": ""} jupyter={"outputs_hidden": false} language="bash"
mypy static_types_example.py --warn-unreachable

# %% [markdown]
# No errors!
# 
# Huge real-life codebases always benefit from adding static type and
# checking the using tools like mypy. These checks can be automated in
# the CI using [pre-commit hooks](https://pre-commit.com) (for instance, the
# [mypy](https://github.com/pre-commit/mirrors-mypy) pre-commit hook) and
# [pre-commit.ci](https://pre-commit.ci).

# %% [markdown]
# ## Hypothesis


# %% [markdown]
# ## Mutation
