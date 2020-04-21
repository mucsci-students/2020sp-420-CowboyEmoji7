"""Initializes and configures Flask and Marshmallow."""
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow
from app_package.memento.command_stack import command_stack
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager


app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SECRET_KEY'] = 'super secret key'
db = SQLAlchemy(app)
ma = Marshmallow(app)
cmd_stack = command_stack()

chromeOptions = Options()
chromeOptions.add_argument("--headless")
chromeOptions.add_argument("--hide-scrollbars")

driver = webdriver.Chrome(ChromeDriverManager().install(), chrome_options=chromeOptions)
driver.get('http://127.0.0.1:5000/')

from app_package import routes
