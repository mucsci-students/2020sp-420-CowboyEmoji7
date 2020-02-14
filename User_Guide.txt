Python:
    - Make sure that python3 is installed on your computer
    - Also make sure that python is located as a path in your enviroment variables

Install virtualenv:
    - Type 'pip install virtualenv'

Create a virtual environment (only done once):
    - Navigate to directory root
    - Type 'virtualenv env'

Install all dependencies:
    - Navigate to the main project folder ('220 cowboy')
    - Activate environment.
        - Type 'env\scripts\activate'
        - If that doesnt work, navigate to your env\scripts and type 'activate'
    - Type 'pip install -r requirements.txt' to install libraries

To create a new Database: 
    - python3 createdb.py (linux/mac) / python createdb.py (windows)

To run the website:
    - python3 run.py (linux/mac) / python run.py (windows)
    