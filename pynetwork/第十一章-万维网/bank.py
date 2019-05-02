"""代码清单11-1 用于创建数据库并与数据库进行通信的程序"""
import os
import pprint
import sqlite3
from collections import namedtuple

def add_payment(conn, debit, credit, dollars, memo):
    """向数据库的表单中添加一条记录"""
    conn.cursor().execute('INSERT INTO payment (debit, credit, dollars, memo) VALUES (?, ?, ?, ?)', (debit, credit, dollars, memo))

def open_database(path='bank.db'):
    """打开数据库，创建一个新表单"""
    db_existed = os.path.exists(path)
    conn = sqlite3.connect(path)
    if not db_existed: #如果以前未创建过数据库文件bank.db
        cursor = conn.cursor()
        cursor.execute('CREATE TABLE payment (id INTEGER PRIMARY KEY, debit TEXT, credit TEXT, dollars INTEGER, memo TEXT)') #创建表单
        cursor.close()
        add_payment(conn, 'brandon', 'psf', 125, 'Registration for PyCon')
        add_payment(conn, 'brandon', 'liz', 200, 'Payment for writing that code')
        add_payment(conn, 'sam', 'brandon', 25, 'Gas money-thanks for the ride!')
        conn.commit() #提交事务，将改动保存进数据库
    return conn

def get_payments_of(conn, account):
    """查询数据库，返回某个帐户涉及的所有借/贷记录"""
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM payment WHERE credit =? or debit=? ORDER BY id', (account, account))
    Row = namedtuple('Row', [field_tuple[0] for field_tuple in cursor.description]) #从最近一次SELECT查询结果中提取字段名
    return [Row(*row) for row in cursor.fetchall()] #将查询结果的每条行记录，都转换成一个具名元组

if __name__ == "__main__":
    conn = open_database()
    pprint.pprint(get_payments_of(conn, 'brandon'))
    conn.close()
