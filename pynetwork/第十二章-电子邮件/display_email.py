"""代码清单12-4 使用EmailMessage读取邮件体及邮件的附件"""
import sys
import argparse
import email.policy

def main(binary_file):
    """读取并打印邮件头、邮件体文本、邮件体中的附件列表"""
    policy = email.policy.SMTP
    msg = email.message_from_binary_file(binary_file, policy=policy)
    for header in ['From', 'To', 'Date', 'Subject']:
        print(header + ':', msg.get(header, '(none)'))
    print()

    try:
        body = msg.get_body(preferencelist=('plain', 'html'))
    except KeyError:
        print('<this message lacks a printable text or HTML body>')
    else:
        print(body.get_content())

    for part in msg.walk():
        cd = part['Content-Disposition']
        is_attachment = cd and cd.split(';')[0].lower() == 'attachment'
        if not is_attachment:
            continue
        content = part.get_content()
        print('* {} attachment named {!r}: {} object of length {}'.format(part.get_content_type(), part.get_filename(), type(content).__name__, len(content)))


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='parse and print an email')
    parser.add_argument('filename', nargs='?', help='file containing an email')
    args = parser.parse_args()
    if args.filename is None:
        main(sys.stdin.buffer)
    else:
        with open(args.filename, 'rb') as fin:
            main(fin)
