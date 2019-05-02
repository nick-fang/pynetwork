"""代码清单11-8 改进的支付应用程序"""
import bank
import uuid
from flask import Flask, abort, flash, get_flashed_messages, redirect, render_template, request, session, url_for

app = Flask(__name__)
app.secret_key = 'saiGeij8AiS2ahleahMo5dahveixuV3J' #这个密钥是怎么跟session扯上关系的？？

@app.route('/login', methods=['GET', 'POST'])
def login():
    username = request.form.get('username', '')
    password = request.form.get('password', '')
    if request.method == 'POST':
        if (username, password) in [('brandon', 'atigdng'), ('sam', 'xyzzy')]:
            session['username'] = username
            session['csrf_token'] = uuid.uuid4().hex #设置session，而非直接设置cookie
            return redirect(url_for('index'))
    return render_template('login.html', username=username) #相比render函数，该函数能够自动转义JS脚本的<>符号？？

@app.route('/logout')
def logout():
    session.pop('username', None)
    return redirect(url_for('login'))

@app.route('/')
def index():
    username = session.get('username') #从服务器数据库中的session中获取帐户名，而非请求头中的cookies中获取
    if not username:
        return redirect(url_for('login'))
    payments = bank.get_payments_of(bank.open_database(), username)
    return render_template('index.html', payments=payments, username=username, flash_messages=get_flashed_messages()) #get_flashed_messages()取出所有保存在session中的flash消息

@app.route('/pay', methods=['GET', 'POST'])
def pay():
    username = session.get('username')
    if not username:
        return redirect(url_for('login'))
    account = request.form.get('account', '').strip() #从html表单中提取信息
    dollars = request.form.get('dollars', '').strip()
    memo = request.form.get('memo', '').strip()
    csrf_token = request.form.get('csrf_token') #从表单中提取隐藏的session ID隐藏属性
    complaint = None
    if request.method == 'POST':
        if csrf_token != session['csrf_token']: #保证攻击者伪造的表单通不过POST请求，即执行不了下方修改数据库的代码
            abort(403)
        if all([account, dollars.isdigit(), memo]):
            db = bank.open_database()
            bank.add_payment(db, username, account, dollars, memo)
            db.commit()
            flash('payment successful') #向session中存进一条flash消息
            return redirect(url_for('index'))
        complaint = ('dollars must be an integer' if not dollars.isdigit() else 'please fill in all three fields')
    return render_template('pay2.html', complaint=complaint, account=account, dollars=dollars, memo=memo, csrf_token=session['csrf_token'])

if __name__ == "__main__":
    app.debug = True
    app.run()
