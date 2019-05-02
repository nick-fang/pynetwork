"""代码清单12-5 手动遍历一个multipart消息的所有部件"""
import sys
import argparse
import email.policy

def walk(part, prefix=''):
    """模拟email模块内置的msg.walk()方法，递归遍历邮件中的所有子部件，直到叶节点"""
    yield prefix, part
    for i, subpart in enumerate(part.iter_parts()):
        yield from walk(subpart, prefix + '.{}'.format(i))

def main(binary_file):
    """解析邮件的结构组成并打印"""
    policy = email.policy.SMTP
    msg = email.message_from_binary_file(binary_file, policy=policy)
    for prefix, part in walk(msg):
        line = '{} type={}'.format(prefix, part.get_content_type())
        if not part.is_multipart():
            content = part.get_content()
            line += ' {} len={}'.format(type(content).__name__, len(content))
            cd = part['Content-Disposition']
            is_attachment = cd and cd.split(';')[0].lower() == 'attachment'
            if is_attachment:
                line += ' attachment'
            filename = part.get_filename()
            if filename is not None:
                line += ' filename={!r}'.format(filename)
        print(line)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='display MIME structure')
    parser.add_argument('filename', nargs='?', help='file containing an email')
    args = parser.parse_args()
    if args.filename is None:
        main(sys.stdin.buffer)
    else:
        with open(args.filename, 'rb') as fin:
            main(fin) #打开并处理待解析的电子邮件二进制文本
