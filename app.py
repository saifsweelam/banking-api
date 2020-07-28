from flask import Flask, request, jsonify, abort

from models import create_models

from datetime import datetime




def create_app(test_config=None):
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
    #GET Accounts
    # curl http://127.0.0.1:5000/accounts
    @app.route('/accounts')
    def get_accounts():
        accounts_query = Account.query
        accounts = accounts_query.all()
        accounts_count = accounts_query.count()

        return jsonify({
            'accounts': accounts,
            'accounts_count': accounts_count
        })

    #GET Accounts
    # curl http://127.0.0.1:5000/accounts
    @app.route('/transactions')
    def get_transactions():
        transactions_query = Transaction.query
        transactions = transactions_query.all()
        transactions_count = transactions_query.count()

        return jsonify({
            'transactions': transactions,
            'transactions_count': transactions_count
        })

    # GET Transaction(only one)
    # curl http://127.0.0.1:5000/transactions/3
    @app.route('/transactions/<int:trans_id>')
    def get_transaction(trans_id):
        trans = Transaction.query.get(trans_id)
        if trans is None:
            abort(404)

        return jsonify({
            'success': True,
            'transaction': trans.serialize()
        })

    # POST Account
    """
    curl -X POST -H "Content-Type:application/json"
    -d '{"name":"ali","type=":"Savings","address":"egy cairo",
    "phone":"01001234567","balance":"1000","active":"true"}'
    http://127.0.0.1:5000/transactions 
    """
    @app.route('/accounts', methods=['POST'])
    def add_account():
        body = request.get_json()
        name = body.get('name')
        account_type = body.get('type')
        address = body.get('address')
        phone = body.get('phone')
        balance = float(body.get('balance'))
        active = bool(body.get('active'))
        try:
            account = Account(
                name=name,
                type=account_type,
                address=address,
                phone=phone,
                balance=balance,
                active=active
            )
            db.session.add(account)
            serialized = account.serialize()
            db.session.commit()
            return jsonify({
                'success': True,
                'created': serialized
            })
        except:
            db.session.rollback()
            abort(422)

    @app.route("/transactions", methods=["POST"])
    def add_transaction():
        body = request.get_json()
        account_id = body.get("account_id", None)
        amount = body.get("amount", None)
        transaction_type = body.get("transaction_type", None)

        # validation
        try:
            account = Account.query.get(account_id)
            if account is None:
                raise Exception("Invalid Account Id")

            new_transaction = Transaction(
                account_id=account_id,
                amount=amount,
                type=transaction_type,
                date=datetime.now()
            )

            if transaction_type.lower() == "withdraw":
                account.balance -= amount
            elif transaction_type.lower() == "deposit":
                account.balance += amount

            # TODO:commit transaction
            db.session.add(new_transaction)
            db.session.commit()
        except Exception as e:
            print(str(e))
            abort(422)
        finally:
            db.session.close()

    @app.route("/accounts/<int:account_id>", methods=['PATCH'])
    def toggle_account_activation(account_id):
        '''Activate and deactivate the account.'''
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
