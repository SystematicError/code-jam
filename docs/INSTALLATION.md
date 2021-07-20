# Installation

### Downloading the project

Firstly you need to download the source code in order to play the game. This can be done through the [git](https://git-scm.com/) command line utility. If you have `git` installed simply run:

```
git clone https://github.com/SystematicError/code-jam
```

If you don't have git installed you may download [this zip archive](https://github.com/SystematicError/code-jam/archive/refs/heads/master.zip).

### Virtual Environments

Perhaps you may not want to install your dependencies for this project globally, if so you can use a [virtualenv](https://virtualenv.pypa.io/en/latest/). Here is how to set it up:

**Windows:**
```
python -m virtualenv venv
venv\Scripts\activate
```

**MacOS and Linux:**
```
python -m virtualenv venv
source venv/bin/activate
```

_Tip: After you are done using the virtualenv type `deactivate` in your terminal and continue on as usual_

### Installing dependencies

After downloading the project, the next step is to install the dependencies. For a quick and simple installation, open up a terminal in the project directory run:

```
pip install -r requirements.txt
```

### Installing dependencies with Poetry

[Poetry](https://python-poetry.org/) is a elegant dependency manager for python. If you have it installed, you can do the following to install the dependencies:

```
poetry install --no-dev
```

_Tip: Remove the `--no-dev` flag if you want to include the development dependencies which includes linters, code formatters, code checkers, etc_

_Note: Poetry has its own virtual environment managing system, to learn more click [here](https://python-poetry.org/docs/managing-environments/)_

### Done already?

Congrats, you have installed Boxed and are ready to go! To launch the program run `python -m boxed` while in the project directory. Make sure to activate your virtualenv if you have one. Go to [Controls](https://github.com/SystematicError/code-jam/tree/master/docs/CONTROLS.md) to master navigation and after that head over to [Game Mechanics](https://github.com/SystematicError/code-jam/tree/master/docs/GAMEPLAY.md) grasp the core mechanics!
