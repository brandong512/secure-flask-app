import sqlite3


def get_balance(account_number, owner):
    try:
        con = sqlite3.connect("bank.db")
        cur = con.cursor()
        # Example of a prepared statements, which protects us from SQL injection
        # attacks. Trying to build queries by building strings/using string interpolation
        # is dangerous and should never be used.
        cur.execute(
            """
            SELECT balance FROM accounts where id=? and owner=?""",
            (account_number, owner),
        )
        row = cur.fetchone()
        if row is None:
            return None
        return row[0]
    finally:
        con.close()


def get_owner_accounts(owner):
    try:
        print("inside: ", owner)
        con = sqlite3.connect("bank.db")
        cur = con.cursor()
        cur.execute(
            """
            SELECT id FROM accounts where owner=?""",
            (owner,),
        )
        rows = cur.fetchall()
        if rows is None:
            return None
        return rows
    finally:
        con.close()


def do_transfer(source, target, amount):
    try:
        con = sqlite3.connect("bank.db")
        cur = con.cursor()
        cur.execute(
            """
            SELECT id FROM accounts where id=?""",
            (target,),
        )
        row = cur.fetchone()
        if row is None:
            return False
        cur.execute(
            """
            UPDATE accounts SET balance=balance-? where id=?""",
            (amount, source),
        )
        cur.execute(
            """
            UPDATE accounts SET balance=balance+? where id=?""",
            (amount, target),
        )
        con.commit()
        return True
    finally:
        con.close()
