from flask import Flask, request, jsonify, abort

from models import create_models

from datetime import datetime


def create_app(test_config=None):
    app = Flask(__name__)
    db_data = create_models(app)

    db = db_data['db']
    Account = db_data['Account']
    Transaction = db_data['Transaction']

    @app.route('/accounts')
    def get_accounts():
        """
        GET Accounts
        curl http://127.0.0.1:5000/accounts
        """
        accounts_query = Account.query
        accounts = accounts_query.all()
        accounts_count = accounts_query.count()

        return jsonify({
            'accounts': [a.serialize for a in accounts],
            'accounts_count': accounts_count
        })

    @app.route('/transactions')
    def get_transactions():
        """
        GET Accounts
        curl http://127.0.0.1:5000/accounts
        """
        transactions_query = Transaction.query
        transactions = transactions_query.all()
        transactions_count = transactions_query.count()

        return jsonify({
            'transactions': [t.serialize for t in transactions],
            'transactions_count': transactions_count
        })

    @app.route('/transactions/<int:trans_id>')
    def get_transaction(trans_id):
        """
        GET Transaction(only one)
        curl http://127.0.0.1:5000/transactions/3
        """
        trans = Transaction.query.get(trans_id)
        if trans is None:
            abort(404)

        return jsonify({
            'success': True,
            'transaction': trans.serialize
        })

    @app.route('/accounts', methods=['POST'])
    def add_account():
        """
        POST Account
        curl -X POST -H "Content-Type:application/json"
        -d '{"name":"ali","type":"Savings","address":"egy cairo",
        "phone":"01001234567","balance":"1000","active":"true"}'
        http://127.0.0.1:5000/accounts 
        """
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
            # Error when return this object "'dict' object is not callable"
            serialized = account.serialize
            db.session.commit()
            return jsonify({
                'success': True,
                'account': serialized
            })
        except Exception as e:
            print(str(e))
            db.session.rollback()
            abort(422)

    @app.route("/transactions", methods=["POST"])
    def add_transaction():
        """
        POST Transaction
        curl http://127.0.0.1:5000/transactions -X POST -H "Content-Type:application/json"
        -d '{"account_id":1, "amount":500.0, "transaction_type":"deposit"}'
        """
        body = request.get_json()
        account_id = body.get("account_id", None)
        amount = body.get("amount", None)
        transaction_type = body.get("transaction_type", None)

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

            db.session.add(new_transaction)
            serialized = new_transaction.serialize
            db.session.commit()

            return jsonify({
                "success": True,
                "transaction": serialized
            })
        except Exception as e:
            print(str(e))
            db.session.rollback()
            abort(422)
        finally:
            db.session.close()

    @app.route("/accounts/<int:account_id>", methods=['PATCH'])
    def toggle_account_activation(account_id):
        '''
        Activate and deactivate the account.
        curl http://127.0.0.1:5000/accounts/1 -X PATCH
        '''
        try:
            account = Account.query.get(account_id)
            if account == None:
                raise Exception("Invalid Account Id")

            account.active = not account.active
            current_status = account.active

            db.session.commit()

            return jsonify({
                "success": True,
                "active": current_status
            })
        except Exception as e:
            print(str(e))
            db.session.rollback()
            abort(422)
        finally:
            db.session.close()

    @app.errorhandler(400)
    def bad_request(error):
        return jsonify({
            'success': False,
            'error': 400,
            'message': 'Bad request'
        }), 400

    @app.errorhandler(404)
    def notfound(error):
        return jsonify({
            'success': False,
            'error': 404,
            'message': 'Resource not found'
        }), 404

    @app.errorhandler(405)
    def not_allowed(error):
        return jsonify({
            'success': False,
            'error': 405,
            'message': 'Method not allowed'
        }), 405

    @app.errorhandler(422)
    def unprocessable(error):
        return jsonify({
            'success': False,
            'error': 422,
            'message': 'Unprocessable entity'
        }), 422

    @app.errorhandler(500)
    def server_error(error):
        return jsonify({
            'success': False,
            'error': 500,
            'message': 'Internal server error'
        }), 500

    return app
