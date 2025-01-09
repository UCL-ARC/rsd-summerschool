# ---
# jupyter:
#   jekyll:
#     display_name: Working with Environments
#   jupytext:
#     notebook_metadata_filter: -kernelspec,jupytext,jekyll
#     text_representation:
#       extension: .py
#       format_name: percent
#       format_version: '1.3'
#       jupytext_version: 1.15.2
# ---

# %% [markdown]
# # Working with Environments
# 
# Virtual environments ensure that your code and the dependencies are
# installed in a locally isolated place, such that the code is reproducible
# (for instance, when filing bug reports) and the correct versions of
# dependencies are installed every time.
# 
# ## Environment solutions by different languages
# 
# Different languages offer different solutions for virtual environment
# management, including standard tools, third-party tools, and environment
# configuration/metadata format.
# 
# - Python
#   - [venv](https://docs.python.org/3/library/venv.html): the barebones implementation
#     for a virtual environment, included in python's standard library
#   - [virtualenv](https://github.com/pypa/virtualenv): Virtual Python Environment builder
#   - [tox](https://tox.wiki/en/latest): virtualenv management and test automation command line tool
#   - [nox](https://nox.thea.codes/en/stable/): command-line tool that automates testing
#     in multiple Python environments
#   - [Pipenv](https://pipenv.pypa.io/en/latest/): Python dev workflow for humans
#   - [uv](https://docs.astral.sh/uv/): an extremely fast Python package and project manager
#   - [conda](https://docs.conda.io/projects/conda/en/latest/user-guide/getting-started.html):
#     powerful command line tool for package and environment management
#   - Several Python build-backends offer frontend utilities and dependency management options:
#     - [Poetry](https://python-poetry.org): Python packaging and dependency management made easy
#     - [Hatch](https://hatch.pypa.io/latest/): a modern, extensible Python project manager
# - Julia
#   - [Pkg](https://docs.julialang.org/en/v1/stdlib/Pkg/): Julia's builtin package and
#     environment manager
# - R
#   - [renv](https://rstudio.github.io/renv/): reproducible environments for your R projects
#   - [conda](https://docs.conda.io/projects/conda/en/latest/user-guide/getting-started.html):
#     powerful command line tool for package and environment management
# - Rust
#   - [Cargo](https://doc.rust-lang.org/cargo/): the Rust package manager
# 
# 
# TODO: Decide on which env management tool to use
