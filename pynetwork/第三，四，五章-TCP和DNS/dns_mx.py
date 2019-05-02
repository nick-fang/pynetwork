"""解析电子邮件域名"""
import argparse
import dns.resolver

def resolve_hostname(hostname, indent=''):
    """解析域名的IPv4和IPv6地址，并显示其规范主机名（如果有）"""
    indent += indent + '    '
    answer = dns.resolver.query(hostname, 'A')
    if answer.rrset:
        for record in answer:
            print(indent, hostname, 'has A address', record.address)
        return
    answer = dns.resolver.query(hostname, 'AAA')
    if answer.rrset:
        for record in answer:
            print(indent, hostname, 'has AAAA address', record.address)
        return
    answer = dns.resolver.query(hostname, 'CNAME')
    if answer.rrset:
        record = answer[0]
        cname = record.address
        print(indent, hostname, 'is a CNAME alias for', cname)
        resolve_hostname(cname, indent)
        return
    print(indent, 'ERROR: no A, AAAA, or CNAME records for', hostname)

def resolve_email_domain(domain):
    """对于“name@domain”这样的邮件地址，解析出它所依赖的邮件服务器的IP地址"""
    try:
        answer = dns.resolver.query(domain, 'MX', raise_on_no_answer=False)
    except dns.resolver.NXDOMAIN:
        print('error: no such domain', domain)
        return
    if answer.rrset:
        records = sorted(answer, key=lambda record: record.preference) #answer是个record元素组成的迭代器，以其元素的preference属性为权重进行排序；records就是重新排序过的answer
        for record in records:
            name = record.exchange.to_text(omit_final_dot=True) #从解析记录（即MX行）中提取出邮件服务器的域名
            print('priority', record.preference)
            resolve_hostname(name) #解析邮件服务器域名的IP地址
    else:
        print('this domain has no explicit MX records')
        print('attempting to resolve it as an A, AAAA or CNAME')
        resolve_hostname(domain)

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='find mailserver IP address')
    parser.add_argument('domain', help='domain that you want to send mail to')
    resolve_email_domain(parser.parse_args().domain)
