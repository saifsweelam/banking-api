from flask import Flask
from flask_sqlalchemy import SQLAlchemy

"""
(Ayman)
GET All Accounts
GET All Transactions


(Ahmed)
GET Transactions by Account ID
POST Acount


(Mohamed Zaitoon)
POST Transaction (Account Balance Must be > 0)
PATCH Account

"""

app = Flask(__name__)