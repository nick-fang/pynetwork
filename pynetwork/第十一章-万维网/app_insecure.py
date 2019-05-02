"""代码清单11-2 一个使用flask框架构建的，不安全的Web应用程序"""
import bank
from flask import Flask, redirect, request, url_for
from jinja2 import Environment, PackageLoader

app = Flask(__name__) #这是一个类实例；__name__就是"__main__"，当前模块的名字？？
get = Environment(loader=PackageLoader(__name__, 'templates')).get_template #这是一个实例方法

@app.route('/login', methods=['GET', 'POST'])
def login():
    username = request.form.get('username', '') #从html表单中提取信息
    password = request.form.get('password', '')
    if request.method == 'POST':
        if (username, password) in [('brandon', 'atigdng'), ('sam', 'xyzzy')]:
            response = redirect(url_for('index')) #重定向到主页
            response.set_cookie('username', username) #使用cookie保存帐户信息
            return response #将包含set-cookie字段的响应报文返回给客户端？？
    return get('login.html').render(username=username) #使用磁盘上的login.html模板来生成html文本

@app.route('/logout')
def logout():
    response = redirect(url_for('login')) #重定向到登录页面
    response.set_cookie('username', '') #清空cookie；这里不安全？？
    return response

@app.route('/')
def index():
    username = request.cookies.get('username')
    if not username:
        return redirect(url_for('login')) #重定向到登录页面
    payments = bank.get_payments_of(bank.open_database(), username) #username帐户的多条借贷记录，是个具名元组组成的列表
    return get('index.html').render(payments=payments, username=username, flash_messages=request.args.getlist('flash'))

@app.route('/pay', methods=['GET', 'POST'])
def pay():
    username = request.cookies.get('username')
    if not username:
        return redirect(url_for('login')) #重定向到登录页面
    account = request.form.get('account', '').strip() #从html表单中提取信息
    dollars = request.form.get('dollars', '').strip()
    memo = request.form.get('memo', '').strip()
    complaint = None
    if request.method == 'POST':
        if all([account, dollars.isdigit(), memo]):
            db = bank.open_database()
            bank.add_payment(db, username, account, dollars, memo)
            db.commit() #提交事务，将改动保存进数据库
            return redirect(url_for('index', flash='payment successful'))
        complaint = ('dollars must be an integer' if not dollars.isdigit() else 'please fill in all three fields')
    return get('pay.html').render(complaint=complaint, account=account, dollars=dollars, memo=memo)

if __name__ == "__main__":
    app.debug = True
    app.run()
