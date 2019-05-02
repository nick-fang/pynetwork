"""代码清单12-6 生成提供国际化支持的电子邮件，用于测试代码清单12-5中的解析脚本"""
import sys
import email.policy
import email.message

text = """\
明了胜于隐晦，
简洁胜于复杂，
复杂胜于混乱，
扁平胜于嵌套。"""

def main():
    msg = email.message.EmailMessage(email.policy.SMTP)
    msg['To'] = '张三 <recipient@example.com>'
    msg['From'] = '李四 <sender@example.com>'
    msg['Subject'] = 'four lines from the wanderer'
    msg['Date'] = email.utils.formatdate(localtime=True)
    msg.set_content(text, cte='quoted-printable')
    sys.stdout.buffer.write(msg.as_bytes())

if __name__ == "__main__":
    main()
