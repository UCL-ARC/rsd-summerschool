# rsd-summerschool

Course materials for Research Software Engineering Summer School.

## Content

In this summer school, you will move beyond programming, to learn how to construct reliable, readable, efficient research software in a collaborative environment. The emphasis is on practical techniques, tips, and technologies to effectively build and maintain complex code. This is an intensive and a practical summer school. The content of each of the 10 half-day units is as follows:

<table>
 <tbody>
  <tr>
   <td>
<h3>Day 1: Version Control</h3>
<ul>
<li>Branching</li>
<li>Rebasing and Merging</li>
<li>Debugging with GitBisect</li>
<li>Forks, Pull Requests and the GitHub Flow</li>
</ul>
   </td>
   <td>
<h3>Day 2: Research Data and Design Patterns in Python</h3>
<ul>
<li>Working with files on the disk</li>
<li>Interacting with the internet</li>
<li>JSON and YAML</li>
<li>Other Scientific Data Formats</li>
<li>Refactoring</li>
<li>Static Typing</li>
<li>Object Orientation</li>
<li>Design Patterns</li>
</ul>
   </td>
  </tr>
  <tr>
<td>
<h3>Day 3: Testing and Code Smell</h3>
<ul>
<li>Why test?</li>
<li>Unit testing and regression testing</li>
<li>Negative testing</li>
<li>Advanced Testing Techniques</li>
<li>Debugging</li>
<li>Continuous Integration</li>
<li>Coding conventions</li>
</ul>
   </td>
   <td>
<h3>Day 4: Packaging and Documenting Software Projects</h3>
<ul>
<li>Turning your code into a package</li>
<li>Releasing code</li>
<li>Documentation</li>
</ul>
   </td>
  </tr>
  <tr>
   <td>
<h3>Day 5: Programming for Speed</h3>
<ul>
<li>Optimisation</li>
<li>Profiling</li>
<li>Scaling laws</li>
<li>NumPy</li>
<li>Miscellaneous libraries</li>
<li>Cython</li>
 </ul>
   </td>
  </tr>
 </tbody>
</table>

## Prerequisites

* You need to be competent in at least one programming language, including concepts like variables, control flow, and functions. This could be through a formal course, a shorter workshop like Software Carpentry, or previous experiences.

* You need to be familiar with the basics of Git and GitHub. A good resource for attendees who are not familiar with Git and GitHub -
  * First 8 chapters of [Version Control with Git by Software Carpentry](https://swcarpentry.github.io/git-novice/)

* You need to be familiar with the foundational libraries of PyData and Scientific Python ecosystem. A good resource for attendees who are not familiar with the Scientific Python ecosystem -
   * [Scientific Python Lectures](https://lectures.scientific-python.org)
      * [1.1. Python scientific computing ecosystem](https://lectures.scientific-python.org/intro/intro.html)
      * [1.2. The Python language](https://lectures.scientific-python.org/intro/language/python_language.html)
      * [1.3.1. The NumPy array object](https://lectures.scientific-python.org/intro/numpy/array_object.html)
      * [1.3.2. Numerical operations on arrays](https://lectures.scientific-python.org/intro/numpy/operations.html)
      * [1.4. Matplotlib: plotting](https://lectures.scientific-python.org/intro/matplotlib/index.html)
      * [1.6. Getting help and finding documentation](https://lectures.scientific-python.org/intro/help/help.html)
   
   If curious, one can also go through the remaining of the [1.3. NumPy: creating and manipulating numerical data](https://lectures.scientific-python.org/intro/numpy/index.html) section and [1.5. SciPy: high-level scientific computing](https://lectures.scientific-python.org/intro/scipy/index.html).
* You are required to bring your own laptop. We have also provided setup instructions for you to install the software needed for the course on your computer.

# Contributing to this repository

This repository contains the course notes as Jupyter notebooks converted into `py:percent` format. This allows to edit the files as plain text as well as jupyter notebooks. To edit them as jupyter notebooks you'll need to have installed jupytext and open the `ipynb.py` files as notebooks via right-click and select "open with" and "notebook" on the Jupyter file browser.

> [!CAUTION]
> Do not run `make` locally on your computer!
> It will produce side effects on your global git configuration (because it will run the scripts from the git chapter)!
> Instead, follow the instructions below.

## Testing it locally

The site is built using gh-actions. If you'd like to test the actions locally,
you can run the actions using [`act`](https://github.com/nektos/act) command
tool. By default this will run the action in a copy of the repository and you
won't be able to inspect the steps that happened. If you'd like to keep the
output in the current directory, use the `-b` (bind) flag.

```bash
$ act -b
[Build website/Build-website] 🚀  Start image=catthehacker/ubuntu:act-latest
[Build website/Build-website]   🐳  docker run image=catthehacker/ubuntu:act-latest platform= entrypoint=["/usr/bin/tail" "-f" "/dev/null"] cmd=[]
[Build website/Build-website] ⭐  Run actions/checkout@v2
[Build website/Build-website]   ✅  Success - actions/checkout@v2
[Build website/Build-website] ⭐  Run actions/cache@v2
INFO[0000]   ☁  git clone 'https://github.com/actions/cache' # ref=v2 
[Build website/Build-website]   ✅  Success - actions/cache@v2
[Build website/Build-website] ⭐  Run Install TeXLive
INFO[0000]   ☁  git clone 'https://github.com/DanySK/setup-texlive-action' # ref=0.1.1 
[Build website/Build-website]   ✅  Success - Install TeXLive
[Build website/Build-website] ⭐  Run Setup Python
INFO[0001]   ☁  git clone 'https://github.com/actions/setup-python' # ref=v2 
[Build website/Build-website]   ✅  Success - Setup Python
[Build website/Build-website] ⭐  Run Install dependencies
INFO[0001]   ☁  git clone 'https://github.com/py-actions/py-dependency-install' # ref=v2 
[Build website/Build-website]   ✅  Success - Install dependencies
[Build website/Build-website] ⭐  Run Building notes
[Build website/Build-website]   ✅  Success - Building notes
[Build website/Build-website] ⭐  Run Builds website
INFO[0001]   ☁  git clone 'https://github.com/helaili/jekyll-action' # ref=v2 
[Build website/Build-website]   🐳  docker run image=act-helaili-jekyll-action-v2:latest platform= entrypoint=[] cmd=[]
[Build website/Build-website]   ✅  Success - Builds website
```

Alternatively, if you want to only run the jekyll build step once you've run the whole action, you can use the official jekyll containers with:

```bash
$ docker run --rm --volume="$PWD:/srv/jekyll" --volume="$PWD/vendor/bundle:/usr/local/bundle" -p 4000:4000 -it jekyll/jekyll:latest jekyll serve
```

and open http://localhost:4000/rsd-engineeringcourse (or the link provided).
Note that this is mounting the `bundle` directory where `act` will create them.


# Migration from jupyter notebooks to py:percent

Using `jupytext` we've converted all the jupyter notebooks into plain text python files (py:percent) with:

```bash
# First cleaned all outputs and commited it
nbstripout --extra-keys metadata.kernelspec ch*/*ipynb
# convert them
find ./ -iname '*ipynb' -exec jupytext --opt notebook_metadata_filter="kernelspec,jupytext,jekyll" --to py:percent {} -o {}.py \;
# then deleted the ipynb
find ./ -iname '*ipynb' -delete
```
