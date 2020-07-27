from flask import Flask, request, jsonify

from models import create_models

from datetime import datetime



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
def create_app(test_config=None):
    app = Flask(__name__)
    db_data = create_models(app)

    db = db_data['db']
    Account = db_data['Account']
    Transaction = db_data['Transaction']

    @app.route("/transactions", methods=["POST"])
    def add_transaction():
        body = request.get_json()
        account_id = body.get("account_id", None)
        amount = body.get("amount", None)
        transaction_type = body.get("transaction_type", None) # TODO: update that key 

        # validation
        try:
            account = Account.query.get(account_id)
            if account is None:
                raise Exception("Invalid Account Id")
            
            new_transaction = Transaction(account_id=account_id,
                                        amount=amount,
                                        account_type=account_type,
                                        date=datetime.now())

            if transaction_type == "Withdraw":
                account.balance -= amount
            elif transaction_type == "Deposit":
                account.balance += amount

            # TODO:commit transaction
            db.session.add(new_transaction) 
            db.session.commit()
        except Exception as e:
            print(str(e))
            abort(422)
        finally:
            db.session.close()

    '''
    Activate and deactivate the account.
    '''
    @app.rout("/accounts/<int:account_id>", methods=['PATCH'])
    def toggel_account_activation(account_id):
        try:
            account = Account.query.get(account_id)
            if account == None:
                raise Exception("Invalid Account Id")

            account.active = not account.active
            # TODO: commit changes
            db.session.commit()
        except Exception as e:
            print(str(e))
            abort(422)
        finally:
            db.session.close()


