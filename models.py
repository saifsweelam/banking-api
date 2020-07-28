from flask_sqlalchemy import SQLAlchemy


def create_models(app):
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///banking.db'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

    db = SQLAlchemy(app)

    class Account(db.Model):
        __tablename__ = 'accounts'

        id = db.Column(db.Integer, primary_key=True)
        name = db.Column(db.String(64), nullable=False)
        type = db.Column(db.String(32), nullable=False)
        address = db.Column(db.String(100))
        phone = db.Column(db.String(32))
        balance = db.Column(db.Float, nullable=False)
        active = db.Column(db.Boolean, default=True)

        transactions = db.relationship('Transaction')

        def __repr__(self):
            return f'<Account {self.id} {self.name} -  {self.balance}:{self.type}> '

        @property
        def serialize(self):
            return {
                'id': self.id,
                'name': self.name
                'type': self.type
                'address': self.address
                'phone': self.phone
                'balance': self.balance
                'active': self.active
            }

    class Transaction(db.Model):
        __tablename__ = 'transactions'

        id = db.Column(db.Integer, primary_key=True)
        account_id = db.Column(db.Integer, db.ForeignKey(
            'accounts.id'), nullable=False)
        amount = db.Column(db.Float, nullable=False)
        type = db.Column(db.String(10))
        date = db.Column(db.DateTime, nullable=False)

        def __repr__(self):
            return f'<Transaction {self.id} {self.account_id} -  {self.amount}:{self.type}> '

        @property
        def serialize(self):
            return {
                'id': self.id,
                'acount_id': self.acount_id
                'type': self.type
                'amount': self.amount
                'date': self.date
            }

    db.create_all()

    return {
        'db': db,
        'Account': Account,
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
