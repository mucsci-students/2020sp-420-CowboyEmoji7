# Cowboy Emoji 7 UML Editor
[![codecov](https://codecov.io/gh/mucsci-students/2020sp-420-CowboyEmoji7/branch/develop/graph/badge.svg)](https://codecov.io/gh/mucsci-students/2020sp-420-CowboyEmoji7)

This project is an open source UML editor built using Flask, jsPlumb, SQLAlchemy, and other useful open source projects. Contains a command line interface, as well as a graphical interface that runs inside your browser. This project exists as a passion project for us at Cowboy Emoji 7--passion for the Unified Modeling Language and, to a lesser extent, passion for passing grades <sup><sup>and degrees</sup></sup>.

# Installation

### Python:
- Make sure that python3 is installed on your computer
- Also make sure that python is located as a path in your enviroment variables

### Install virtualenv:
- Type `pip install virtualenv`

### Create a virtual environment (only done once):
- Navigate to directory root
- Type `virtualenv env`

**Here is where different operating systems require different commands.**
- [Windows Installation](#windows)
- [Linux/Mac Installation](#linux-or-mac)



## LINUX or MAC

### Install all dependencies:
- Navigate to the main project folder (*'220 cowboy'*)
- Activate environment.
	- Type `source env/bin/activate`
- Type `python3 install.py` to install libraries

***The operation below assumes you are inside of the activated enviroment***

### To run the application:
- `python3 run.py`
- If you would like the web view, type `web` in the console that appears

## WINDOWS

### Install all dependencies:
- Navigate to the main project folder (*'220 cowboy'*)
- Activate environment.
	- Type `env\Scripts\activate`
- Type `python install.py` to install libraries

***The operation below assumes you are inside of the activated enviroment***

### To run the application:
- python run.py
- If you would like the web view, type 'web' in the console that appears

# Tests
We have a continuous integration setup that runs our current suite of pytest tests with every push and pull request.

*pytest tests can be found in /tests/ , feel free to contribute*

To run tests manually, ensure pytest is installed on your system and run 'pytest' in the top level of the project.

# Use
See [our user guide](USERGUIDE.md)

# Contribute
See [our contributing guide](CONTRIBUTING.md) and [code of conduct](CODE_OF_CONDUCT.md)

# License
See [our license](LICENSE) and [notice](NOTICE.txt)
