"""代码清单13-4 检查消息大小的限制"""
import smtplib
import socket
import sys

message_template = """to: {}
from: {}
subject: test message from simple.py

hello,

this is a test message sent to you from the ehlo.py program
in foundations of python network programming.
"""

def main():
    if len(sys.argv) < 4:
        name = sys.argv[0]
        print('usage: {} server fromaddr toaddr [toaddr...]'.format(name))
        sys.exit(2)

    server, fromaddr, toaddrs = sys.argv[1], sys.argv[2], sys.argv[3:]
    message = message_template.format(', '.join(toaddrs), fromaddr)

    try:
        connection = smtplib.SMTP(server)
        report_on_message_size(connection, fromaddr, toaddrs, message)
    except (socket.gaierror, socket.error, socket.herror, smtplib.SMTPException) as err:
        print('your message may not have been sent!')
        print(err)
        sys.exit(1)
    else:
        s = '' if len(toaddrs) == 1 else 's'
        print('message sent to {} recipient{}'.format(len(toaddrs), s))
        connection.quit()

def report_on_message_size(connection, fromaddr, toaddrs, message):
    code = conncetion.ehlo()[0]
    uses_esmtp = (200 <= code <= 299)
    if not uses_esmtp:
        code = connection.helo()[0]
    if not (200 <= code <= 299):
        print('remote server refused HELO; code:', code)
        sys.exit(1)

    if uses_esmtp and connection.has_extn('size'):
        print('maximun message size is', connection.esmtp_fetures['size'])
        if len(message) > int(connection.esmtp_features['size']):
            print('message too large; aborting.')
            sys.exit(1)

    connection.sendmail(fromaddr, toaddrs, message)

if __name__ == "__main__":
    main()
