# ---
# jupyter:
#   jekyll:
#     display_name: Scaling
#   jupytext:
#     notebook_metadata_filter: -kernelspec,jupytext,jekyll
#     text_representation:
#       extension: .py
#       format_name: percent
#       format_version: '1.3'
#       jupytext_version: 1.17.2
# ---

# %% [markdown]
# # Scaling for containers and algorithms
#
# We've seen that NumPy arrays are really useful. Why wouldn't we always want to use them for data which is all the same type?

# %%
import numpy as np
from timeit import repeat
from matplotlib import pyplot as plt
# %matplotlib inline

# %% [markdown]
# Let's look at appending data into a NumPy array, compared to a plain Python list: 

# %%
def time_append_to_ndarray(count):
    # the function repeat does the same that the `%timeit` magic
    # but as a function; so we can plot it.
    return repeat('np.append(before, [0])',
                  f'import numpy as np; before=np.ndarray({count})',
                  number=10000)


# %%
def time_append_to_list(count):
    return repeat('before.append(0)',
                  f'before = [0] * {count}',
                  number=10000)


# %%
counts = np.arange(1, 100000, 10000)

def plot_time(function, counts, title=None):
    plt.plot(counts, list(map(function, counts)))
    plt.ylim(bottom=0) 
    plt.ylabel('seconds')
    plt.xlabel('array size')
    plt.title(title or function.__name__)


# %%
plot_time(time_append_to_list, counts)

# %%
plot_time(time_append_to_ndarray, counts)


# %% [markdown]
# Adding an element to a Python list is way faster! Also, it seems that adding an element to a Python list is independent of the length of the list, but it's not so for a NumPy array.
#
# How do they perform when accessing an element in the middle?

# %%
def time_lookup_middle_element_in_list(count):
    before = [0] * count
    def totime():
        x = before[count // 2]
    return repeat(totime, number=10000)


# %%
def time_lookup_middle_element_in_ndarray(count):
    before = np.ndarray(count)
    def totime():
        x = before[count // 2]
    return repeat(totime, number=10000)



# %%
plot_time(time_lookup_middle_element_in_list, counts)

# %%
plot_time(time_lookup_middle_element_in_ndarray, counts)

# %% [markdown]
# Both scale well for accessing the middle element.
#
# What about inserting at the beginning?
#
# If we want to insert an element at the beginning of a Python list we can do:

# %%
x = list(range(5))
x

# %%
x[0:0] = [-1]
x


# %%
def time_insert_to_list(count):
    return repeat('before[0:0] = [0]',
                  f'before = [0] * {count}',number=10000)


# %%
plot_time(time_insert_to_list, counts)

# %% [markdown]
# `list` performs **badly** for insertions at the beginning!
#
# There are containers in Python that work well for insertion at the start:

# %%
from collections import deque


# %%
def time_insert_to_deque(count):
    return repeat('before.appendleft(0)', 
                  f'from collections import deque; before = deque([0] * {count})',
                  number=10000)


# %%
plot_time(time_insert_to_deque, counts)

# %% [markdown]
# But looking up in the middle scales badly:

# %%
def time_lookup_middle_element_in_deque(count):
    before = deque([0] * count)
    def totime():
        x = before[count // 2]
    return repeat(totime, number=10000)

# %%
plot_time(time_lookup_middle_element_in_deque, counts)

# %% [markdown]
# What is going on here?
#
# Arrays are stored as contiguous memory. Anything which changes the length of the array requires the whole array to be copied elsewhere in memory.
#
# This copy takes time proportional to the array size.
#
# ![Adding an element to an array - memory representation](./array_memory.svg)
#
# The Python `list` type is **also** an array, but it is allocated with **extra memory**. Only when that memory is exhausted is a copy needed.
#
# ![Adding an element to a list - memory representation](list_memory.svg)
#
# If the extra memory is typically the size of the current array, a copy is needed every 1/N appends, and costs N to make, so **on average** copies are cheap. We call this **amortized constant time**. 
#
# This makes it fast to look up values in the middle. However, it may also use more space than is needed.
#
# The deque type works differently: each element contains a pointer to the next. Inserting elements is therefore very cheap, but looking up the Nth element requires traversing N such pointers.
#
# ![Adding an element to a deque - memory representation](deque_memory.svg)
#

# %% [markdown]
# In conclusion, NumPy arrays are optimal if you know the size of your data from the beginning, and you will not have to
# change their size frequently (or at all). For dynamic data, it pays off to choose the right data container for your problem.
