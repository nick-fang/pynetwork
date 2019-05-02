"""代码清单13-5 选择性地使用tls"""
import sys
import smtplib
import socket
import ssl

message_template = """to: {}
from: {}
subject: test message from simple.py

hello,

this is a test message sent to you from the tls.py program
in foundations of python network programming.
"""

def main():
    if len(sys.argv) < 4:
        name = sys.argv[0]
        print('syntax: {} server fromaddr toaddr [toaddr...]'.format(name))
        sys.exit(2)

    server, fromaddr, toaddrs = sys.argv[1], sys.argv[2], sys.argv[3:]
    message = message_template.format(', '.join(toaddrs), fromaddr)

    try:
        connection = smtplib.SMTP(server)
        send_message_securely(connection, fromaddr, toaddrs, message)
    except (socket.gaierror, socket.error, socket.herror, smtplib.SMTPException) as err:
        print('your message may not have been sent!')
        print(err)
        sys.exit(1)
    else:
        s = '' if len(toaddrs) == 1 else 's'
        print('message sent to {} recipient{}'.format(len(toaddrs), s))
        connection.quit()

def send_message_securely(connection, fromaddr, toaddrs, message):
    code = connection.ehlo()[0]
    uses_esmtp = (200 <= code <= 299)
    if not uses_esmtp:
        code = connection.helo[0]
        if not (200 <= code <= 299):
            print('remove server refused HELO; code:', code)
            sys.exit(1)

    if uses_esmtp and connection.has_extn('starttls'):
        print('negotiating tls...')
        context = ssl.SSLContext(ssl.PROTOCOL_SSLv23)
        context.set_default_verify_paths()
        context.verify_mode = ssl.CERT_REQUIRED
        connection.starttls(context=context)
        code = connection.ehlo()[0]
        if not (200 <= code <= 299):
            print('could not EHLO after STARTTLS')
            sys.exit(5)
        print('using TLS connection.')
    else:
        print('server does not support TLS; using normal connection.')

    connection.sendmail(fromaddr, toaddrs, message)

if __name__ == "__main__":
    main()
