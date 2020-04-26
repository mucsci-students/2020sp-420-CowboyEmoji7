"""Initializes and configures Flask and Marshmallow."""
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow
from app_package.memento.command_stack import command_stack
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager
from webdriver_manager.firefox import GeckoDriverManager
import threading
import logging
import sys
import io

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SECRET_KEY'] = 'super secret key'
db = SQLAlchemy(app)
ma = Marshmallow(app)
cmd_stack = command_stack()

suppress_early = io.StringIO()
sys.stdout = suppress_early

cli = sys.modules['flask.cli']
cli.show_server_banner = lambda *x: None

log = logging.getLogger('werkzeug')
log.setLevel(logging.ERROR)

thread = threading.Thread(target=app.run, kwargs={'port': 5000, 'debug': False}, daemon=True)
thread.start()

driverOptions = Options()
driverOptions.add_argument("--headless")
driverOptions.add_argument("--hide-scrollbars")
driverOptions.add_experimental_option('excludeSwitches', ['enable-logging'])


#driver = webdriver.Chrome(ChromeDriverManager().install(), chrome_options=driverOptions)
driver = 'null'
try:
    driver = webdriver.Firefox(GeckoDriverManager().install(), firefox_options=driverOptions)
except:
    print('\nFirefox installation not found, attempting to use Chrome.\n')
    try:
        driver = webdriver.Chrome(ChromeDriverManager().install(), chrome_options=driverOptions)
    except: # pragma: no cover
        print('Chrome installation not found, ensure Firefox or Chrome are installed to utilize export functionality.\n')
driver.get('http://127.0.0.1:5000/')

from app_package import routes

sys.stdout.flush()
sys.stdout = sys.__stdout__