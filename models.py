from flask_sqlalchemy import SQLAlchemy


def create_models(app):
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///banking.db'

    db = SQLAlchemy(app)

    class Account(db.Model):
    
    class Transaction(db.Model):

    return {
        'db': db
        'Account': Account
        'Transaction': Transaction
    }

"""
Account
{
    id : int
    name : str
    type : str
    address : str
    phone : str
    balance : float (min=0)
    active : bool
}

Transaction
{
    id : int
    acount_id : int
    amount : float (min=0)
    type : str
    date : datetime
}
"""