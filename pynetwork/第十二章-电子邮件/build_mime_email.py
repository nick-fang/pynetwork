"""代码清单12-3 构造包含HTML、内嵌图片以及附件的MIME格式电子邮件"""
import sys
import argparse
import email.message
import email.policy
import email.utils
import mimetypes

PLAIN = """hello, 
this is a MIME message from chapter 12. 
- anonymous"""

HTML = """<p>hello,</p>
<p>this is a <b>test message</b> from chapter 12.</p>
<p>- <i>anonymous</i></p>"""

IMG = """<p>this is the smallest possible blue GIF:</p>
<img src="cid:{}" height="80" width="80">"""

#来自 http://www.perlmonks.org/?node_id=7974 的示例gif图片
BLUE_DOT = (b'GIF89a1010\x900000\xff000,000010100\x02\x02\x0410;'.replace(b'0', b'\x00').replace(b'1', b'\x01'))

def main(args):
    """构建并打印一份电子邮件"""
    msg = email.message.EmailMessage(email.policy.SMTP)
    msg['To'] = 'Test Recipient <recipient@example.com>'
    msg['From'] = 'Test Sender <sender@example.com>'
    msg['Subject'] = 'Foundations of python network programming'
    msg['Date'] = email.utils.formatdate(localtime=True)
    msg['Message-ID'] = email.utils.make_msgid()

    if not args.i:
        msg.set_content(HTML, subtype='html')
        msg.add_alternative(PLAIN)
    else:
        cid = email.utils.make_msgid()
        msg.set_content(HTML + IMG.format(cid.strip('<>')), subtype='html')
        msg.add_related(BLUE_DOT, 'image', 'gif', cid=cid, filename='blue-dot.gif')
        msg.add_alternative(PLAIN)

    for filename in args.filename:
        mime_type, encoding = mimetypes.guess_type(filename)
        if encoding or (mime_type is None):
            mime_type = 'application/octet-stream'
        main_type, sub_type = mime_type.split('/')
        if main_type == 'text':
            with open(filename, encoding='utf-8') as fin:
                text = fin.read()
            msg.add_attachment(text, sub_type, filename=filename)
        else:
            with open(filename, 'rb') as fin:
                data = fin.read()
            msg.add_attachment(data, main_type, sub_type, filename=filename)
    sys.stdout.buffer.write(msg.as_bytes())

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='build, print a MIME email')
    parser.add_argument('-i', action='store_true', help='include gif image')
    parser.add_argument('filename', nargs='*', help='attachment filename')
    main(parser.parse_args())
