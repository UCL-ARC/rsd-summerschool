# ---
# jupyter:
#   jekyll:
#     display_name: Miscellaneous libraries
#   jupytext:
#     notebook_metadata_filter: -kernelspec,jupytext,jekyll
#     text_representation:
#       extension: .py
#       format_name: percent
#       format_version: '1.3'
#       jupytext_version: 1.17.2
# ---

# %% [markdown]
# # Miscellaneous libraries to improve your code's performance
#
# Over the course of years, Python ecosystem has developed more and more solutions
# to combat the relatively slow performance of the language. As seen in the previous
# lessons, the speed of computation matters quite a lot while using a technology
# in scientific setting. This lesson introduces a few such popular libraries that have
# been widely adopted in the scientific use of Python.
#
# We will only look at Numba, but please browse the notes for the rest of the
# libraries at your leisure.
#
# ## Compiling Python code
#
# We know that Python is an interpreted and not a compiled language, but is there a way
# to compile Python code? There are a few libraries/frameworks that lets you
# [*just in time*][wiki-jit] (JIT) or [*ahead of time*][wiki-aot] (AOT) compile Python code. Both the techniques allow
# users to compile their Python code without using any explicit low level langauge's
# bindings, but both the techniques are different from each other.
#
# [wiki-jit]: https://en.wikipedia.org/wiki/Just-in-time_compilation
# [wiki-aot]: https://en.wikipedia.org/wiki/Ahead-of-time_compilation
#
# Just in time compilers compile functions/methods at runtime whereas ahead of time
# compilers compile the entire code before runtime. AOT can do much more compiler
# optimizations than JIT, but AOT compilers produce huge binaries and that too only
# for specific platforms. JIT compilers have limited optimization routines but they
# produce small and platform independent binaries.
#
# JIT and AOT compilers for Python include, but are not limited to -
#  - [Numba](http://numba.pydata.org): a Just-In-Time Compiler for Numerical Functions in Python
#  - [mypyc](https://mypyc.readthedocs.io/en/latest/introduction.html): compiles Python modules to C extensions using standard Python type hints
#  - [JAX](https://jax.readthedocs.io/en/latest/jit-compilation.html): a Python library for accelerator-oriented array computation and program transformation
#
# Although all of them were built to speed-up Python code, each one of them is a bit
# different from each other when it comes to their use-case.
#
# ### Numba
#
# Numba is an open source JIT compiler that translates a subset of Python and NumPy code
# into fast machine code. The good thing about Numba is that it works on plain Python
# loops and one doesn't need to configure any compilers manually to JIT compile Python code.
# Another good thing is that it understands NumPy natively, but as detailed in its
# documentation, it only understands a subset of NumPy functionalities.
#
# Numba provides users with an easy to use function decorator - `jit`. Let's start by
# importing the libraries we will use in this lesson.
#

# %%
import math

from numba import jit, njit
import numpy as np

# %% [markdown]
# We can mark a function to be JIT compiled by decorating it
# with numba's `@jit`. The decorator takes a `nopython` argument that tells Numba to
# enter the compilation mode and not fall back to usual Python execution.
#
# Here, we are showing a usual python function, and one that's decorated. 
# We don't need to duplicate and change its name when using numba, but we want to keep both of them here to compare their execution times.

# %%
def f(x):
    return np.sqrt(x)

@jit(nopython=True)
def jit_f(x):
    return np.sqrt(x)

# %% [markdown]
# It looks like the `jit` decorator should make our Numba compile our function
# and make it much faster than the non-jit version. Let's test this out.
#
# Note that the first function call is not included while timing because that
# is where Numba compiles the function. The compilation at runtime is called
# just in time compilation and resultant binaries are cached for the future
# runs. 

# %%
data = np.random.uniform(low=0.0, high=100.0, size=1_000)

# %%
# %%timeit
f(data)

# %%
# %%timeit -n 1 -r 1
_ = jit_f(data)  # compilation and run

# %%
# %%timeit
jit_f(data)  # just run

# %% [markdown]
# Surprisingly, the JITted function was slower than plain Python and NumPy
# implementation! Why did this happen? Numba does not provide valuable performance
# gains over pure Python or NumPy code for simple operations and small dataset.
# The JITted function turned out to be slower than the non-JIT implementation
# because of the compilation overhead. Note that the result from the compilation
# run could be very noisy and could give a higher than real value, as mentioned
# in the previous lessons. Let's try increasing the size of our
# data and perform a non-NumPy list comprehension on the data.
#
# The `jit` decorator with `nopython=True` is so widely used there exists an alias
# decorator for the same - `@njit`

# %%
data = np.random.uniform(low=0.0, high=100.0, size=1_000_000)


# %%
def f(x):
    return [math.sqrt(elem) for elem in x]

@njit
def jit_f(x):
    return [math.sqrt(elem) for elem in x]

# %%
# %%timeit
f(data)

# %%
# %%timeit -n 1 -r 1
_ = jit_f(data)  # compilation and run

# %%
# %%timeit
jit_f(data)  # just run

# %% [markdown]
# That was way faster than the non-JIT function! But, the result was still slower
# than the NumPy implementation. NumPy is still good for relatively simple
# computations, but as the complexity increases, Numba functions start
# outperforming NumPy implementations.
#
# Let's go back to our plain Python mandelbrot code from the previous lessons and
# JIT compile it -

# %%
@njit
def mandel1(position, limit=50):
    
    value = position
    
    while abs(value) < 2:
        limit -= 1        
        value = value**2 + position
        if limit < 0:
            return 0
        
    return limit

xmin = -1.5
ymin = -1.0
xmax = 0.5
ymax = 1.0
resolution = 300
xstep = (xmax - xmin) / resolution
ystep = (ymax - ymin) / resolution
xs = [(xmin + (xmax - xmin) * i / resolution) for i in range(resolution)]
ys = [(ymin + (ymax - ymin) * i / resolution) for i in range(resolution)]

# %%
# %%timeit -n 1 -r 1
data = [[mandel1(complex(x, y)) for x in xs] for y in ys]  # compilation and run

# %%
# %%timeit
data = [[mandel1(complex(x, y)) for x in xs] for y in ys]  # just run

# %% [markdown]
# The compiled code already beats our fastest NumPy implementation! It is not
# necessary the compiled code will perform better than NumPy code, but it usually
# gives performance gains for signifantly large computations. As always, it is
# good to measure the performance to check if there are any gains.
