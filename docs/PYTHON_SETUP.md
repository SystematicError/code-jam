# Setting up python

This section of the documentation is aimed towards users who have never used python before and are interested in setting it up. If you already have Python and PIP installed you may proceed to the [installation](https://github.com/SystematicError/code-jam/tree/master/docs/INSTALLATION.md) section.


### Checking if python is installed

Firstly check if you have python installed in your system, if you're on Linux you probably already have python installed, if you don't or have another operating system, don't worry as we are going to go over it.

Usually when python is installed it is added to path; open up your terminal and type `python` or `python3`. If this up a shell like the following:

```
Python 3.9.5 (default, May 24 2021, 12:50:35)
[GCC 11.1.0] on linux
Type "help", "copyright", "credits" or "license" for more information.
>>>
```

then congrats, you have Python installed and on Path! If it does not show up then you probably don't have it installed or on path.

### Installing python

Visit [Python's Official Website](https://www.python.org/downloads/) and follow the choose the appropriate version (ones with the major version `3.9` are recommended). You may use a package manager if you wish so. If you want to manage multiple python installations, check out [pyenv](https://github.com/pyenv/pyenv).

_Tip: Make sure to choose the "Add to path" when running the installer_

### Installing PIP

PIP is Python's dependency manager, if you installed using the above method then you should have it already, if not follow the instructions given [here](https://pip.pypa.io/en/stable/installing/).

### Verifying your python version

In your terminal type `python --version` or `python3 --version`. It should return something like the following:

```
Python 3.9.5
```

It is recommended that the major version be `3.9`, however older `3.x` installations may work. Any `2.x` version is absolutely not viable and should be upgraded.

### Made it so far?

[Check out how to install the actual project!](https://github.com/SystematicError/code-jam/tree/master/docs/INSTALLATION.md)
