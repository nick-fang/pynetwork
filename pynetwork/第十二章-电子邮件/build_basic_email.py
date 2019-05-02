"""代码清单12-2 生成一个包含简单文本的电子邮件消息"""
import sys
from email import message, policy, utils

TEXT = """hello, 
this is a basic message from chapter 12. 
- anonymous"""

def main():
    """构建并打印一封电子邮件"""
    msg = message.EmailMessage(policy.SMTP)
    msg['To'] = 'test recipient <recipient@example.com>'
    msg['From'] = 'test sender <sender@example.com>'
    msg['Subject'] = 'test message, chapter 12'
    msg['Date'] = utils.formatdate(localtime=True)
    msg['Message-ID'] = utils.make_msgid()
    msg.set_content(TEXT)
    sys.stdout.buffer.write(msg.as_bytes())

if __name__ == "__main__":
    main()
