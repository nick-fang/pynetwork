"""一个包含递归的简单DNS查询"""
import argparse
import dns.resolver

def lookup(name):
    """查询name代表的主域名下的各个服务器主机域名/IP地址"""
    for qtype in ['A', 'AAAA', 'CNAME', 'MX', 'NS']: #查询的主机类型，分别表示该主域名的IPv4地址、该主域名的IPv6地址、该主域名的规范主机名、主域名下的邮件服务器、主域名下的DNS服务器
        answer = dns.resolver.query(name, qtype, raise_on_no_answer=False)
        if answer.rrset:
            print(answer.rrset)

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='resolver a name using DNS')
    parser.add_argument('name', help='name that you want to look up in DNS')
    lookup(parser.parse_args().name)
