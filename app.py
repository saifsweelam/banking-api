from flask import Flask

from models import create_models

app = Flask(__name__)
db_data = create_models(app)

db = db_data['db']
Account = db_data['Account']
Transaction = db_data['Transaction']

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
