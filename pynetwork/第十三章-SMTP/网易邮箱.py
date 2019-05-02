"""使用三种模式发送电子邮件：1、非加密模式；2、465端口下使用SMTP_SSL()类进行加密；3、25端口下使用.starttls()方法进行加密"""

import smtplib

USERNAME = 'caihuyougui@126.com'
PASSWORD = 'zyx38795332'
fromaddr = 'caihuyougui@126.com'
toaddrs = ['coal@live.cn']
message = '''To: coal@live.cn
From: caihuyougui@126.com
Subject: Hello world

hello world, customer!
'''

server = smtplib.SMTP(host='smtp.126.com', port=25)
server.set_debuglevel(True)
server.login(USERNAME, PASSWORD)
server.sendmail(fromaddr, toaddrs, message)
server.quit()



import smtplib
import ssl

USERNAME = 'caihuyougui@126.com'
PASSWORD = 'zyx38795332'
fromaddr = 'caihuyougui@126.com'
toaddrs = ['coal@live.cn']
message = '''To: coal@live.cn
From: caihuyougui@126.com
Subject: Hello world

hello world, customer!
'''

context = ssl.create_default_context()
server = smtplib.SMTP_SSL(host='smtp.126.com', port=465, context=context)
server.set_debuglevel(True)
server.sock #套接字类型为SSL_socket
server.sock.version() #查看双方协商后使用的加密协议版本，包括"SSLv2", "SSLv3", "TLSv1", "TLSv1.1" 和 "TLSv1.2"
server.login(USERNAME, PASSWORD)
server.sendmail(fromaddr, toaddrs, message)
server.quit()




context = ssl.create_default_context()
server = smtplib.SMTP(host='smtp.126.com', port=25)
server.set_debuglevel(True)
server.sock #套接字类型为TCP
server.ehlo() #提前调用ehlo命令后，才能检查ESMTP特性
if server.has_extn('starttls'):
    server.starttls(context=context)
server.sock #可以发现套接字类型从TCP转变成了SSL，但是端口仍旧是25没变
server.sock.version() #查看双方协商后使用的加密协议版本
server.login(USERNAME, PASSWORD)
server.sendmail(fromaddr, toaddrs, message)
server.quit()




context = ssl.create_default_context()
with smtplib.SMTP(host='smtp.126.com', port=25) as server: # with块会隐式调用server.quit()
    server.ehlo()
    if server.has_extn('starttls'):
        server.starttls(context=context)
    server.login(USERNAME, PASSWORD)
    server.sendmail(fromaddr, toaddrs, message)




import smtplib
import ssl

USERNAME = 'caihuyougui@qq.com'
PASSWORD = 'bpnqywrigcvcbccg'
fromaddr = 'caihuyougui@qq.com'
toaddrs = ['coal@live.cn']
message = '''To: coal@live.cn
From: caihuyougui@qq.com
Subject: Hello world

hello world, customer!
'''

context = ssl.create_default_context()
server = smtplib.SMTP_SSL(host='smtp.qq.com', port=465, context=context)
server.set_debuglevel(True)
server.login(USERNAME, PASSWORD)
server.sendmail(fromaddr, toaddrs, message)
server.quit()

server2=smtplib.SMTP(host='smtp.qq.com', port=587)
server2.set_debuglevel(True)
server2.sock
server2.starttls(context=context)
server2.sock
server2.login(USERNAME, PASSWORD)
server2.sendmail(fromaddr, toaddrs, message)
server2.quit()
