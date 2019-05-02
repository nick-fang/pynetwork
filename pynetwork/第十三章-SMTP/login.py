"""代码清单13-6 SMTP认证"""
import sys
import smtplib
import socket
from getpass import getpass

message_template = """to: {}
from: {}
subject: test message from simple.py

hello,

this is a test message sent to you from the login.py program
in foundations of python network programming.
"""

def main():
    if len(sys.argv) < 4:
        name = sys.argv[0]
        print('syntax: {} server fromaddr toaddr [toaddr...]'.format(name))
        sys.exit(2)

    server, fromaddr, toaddrs = sys.argv[1], sys.argv[2], sys.argv[3:]
    message = message_template.format(', '.join(toaddrs), fromaddr)
    username=input('enter username: ')
    password=getpass('enter password: ')

    try:
        connection=smtplib.SMTP(server)
        try:
            connection.login(username, password)
        except smtplib.SMTPException as err:
            print('authentication failed:', err)
            sys.exit(1)
        connection.sendmail(fromaddr, toaddrs, message)
    except (socket.gaierror, socket.error, socket.herror, smtplib.SMTPException) as err:
        print('your message may not have been sent!')
        print(err)
        sys.exit(1)
    else:
        s='' if len(toaddrs)==1 else 's'
        print('message sent to {} recipient{}'.format(len(toaddrs), s))
        connection.quit()

if __name__ == "__main__":
    main()
