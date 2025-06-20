---
title: Linux
---

Linux
=====

Package Manager
---------------

Linux users should be able to use their package manager to install all of this software (if you're
using Linux, we assume you won't have any trouble with these requirements).

However note that if you are running an older Linux distribution you may get older versions with
different look and features. A recent Linux distribution is recommended.

Python via package manager
--------------------------

Recent versions of Ubuntu pack mostly up to date versions of all needed
packages. The version of IPython might be slightly out of date. Advanced users may wish to upgrade
this using ```pip``` or a manual install. On Ubuntu you should ensure that the following packages
are installed using apt-get.

*  python3-numpy
*  python3-scipy
*  python3-pytest
*  python3-matplotlib
*  python3-pip
*  jupyter
*  ipython3
*  ipython3-notebook

Older distributions may have outdated versions of specific packages.
Other linux distributions most likely also contain the needed python packages but again
they may also be outdated.

Git
---

If git is not already available on your machine you can try to install it via your distribution
package manager (e.g. `apt-get` or `yum`), for example:

``` bash
sudo apt-get install git
```

Editor
------

Many different text editors suitable for programming are available.  If you don't already have a
favourite, you could look at [Visual Studio Code](https://code.visualstudio.com/).
Check [their setup page](https://code.visualstudio.com/docs/setup/linux) for detailed
instructions.

For a better git integration we suggest the [git
graph](https://marketplace.visualstudio.com/items?itemName=mhutchie.git-graph)
plugin.

Regardless of which editor you have chosen you should configure git to use it. Executing something
like this in a terminal should work:

``` bash
git config --global core.editor NameofYourEditorHere
```

The default shell is usually bash but if not you can get to bash by opening a terminal and typing
`bash`.
