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

***Both operations below assume you are inside of the activated enviroment***

### To create a new Database: 
- Type `python3 createdb.py`
- If a warning containing (*SQLALCHEMY_TRACK_MODIFICATIONS*) is thrown it can be safely ignored

### To run the application:
- `python3 run.py`
- If you would like the web view, type `web` in the console that appears

## WINDOWS

### Install all dependencies:
- Navigate to the main project folder (*'220 cowboy'*)
- Activate environment.
	- Type `env\Scripts\activate`
- Type `python install.py` to install libraries

***Both operations below assume you are inside of the activated enviroment***

### To create a new Database: 
- `python createdb.py`
- If a warning containing (*SQLALCHEMY_TRACK_MODIFICATIONS*) is thrown it can be safely ignored

### To run the application:
- python run.py
- If you would like the web view, type 'web' in the console that appears

