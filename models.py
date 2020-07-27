from flask_sqlalchemy import SQLAlchemy


def create_models(app):
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///banking.db'

    db = SQLAlchemy(app)

    class Account(db.Model):
    
    class Transaction(db.Model):
    __tablename__ = 'transactions'

    id = db.Column(db.Integer, primary_key=True)
    account_id= db.Column(db.Integer,db.ForeignKey('accounts.id'), nullable=False)
    amount = db.Column(db.Float, nullable=False)
    type = db.Column(db.String(10))
    date = db.Column(db.DateTime, nullable=False)
    def __repr__(self):
      return f'<Transaction {self.id} {self.account_id} -  {self.amount}:{self.type}> '

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