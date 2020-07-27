from flask_sqlalchemy import SQLAlchemy


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