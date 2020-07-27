from flask import Flask
from flask_sqlalchemy import SQLAlchemy

"""

GET All Accounts
GET All Transactions
GET Transactions by Account ID

POST Acount
POST Transaction (Account Balance Must be > 0)

PATCH Account

"""

app = Flask(__name__)