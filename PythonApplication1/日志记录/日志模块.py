
import logging
logging.basicConfig(level=logging.DEBUG, format=' %(asctime)s - %(levelname)s - %(message)s')
logging.debug('start of program')

def factorial(n):
    logging.debug('start of factorial({})'.format(n))
    total=1
    for i in range(1, n+1):
        total*=i
        logging.debug('i is {}, total is {}'.format(i, total))
    logging.debug('end of factorial({})'.format(n))
    return total

print(factorial(5))
logging.debug('end of program')



import logging
logging.basicConfig(level=logging.INFO, format=' %(asctime)s - %(levelname)s - %(message)s') #设置日志消息的打印格式
logging.debug('some debugging details.') #直接在命令行中打印日志消息；5种日志级别，对应5个打印日志的函数
logging.info('the logging module is working.')
logging.warning('an error message is about to be logged.')
logging.error('an error has occurred.')
logging.critical('the program is unable to recover!')
logging.disable(logging.ERROR)
logging.critical('critical error! critical error!')
logging.error('error! error!')



import logging
logging.basicConfig(filename='my_program_log.txt', level=logging.DEBUG, format='%(asctime)s - %(levelname)s - %(message)s')
logging.debug('some debugging details.') #直接在命令行中打印日志消息；5种日志级别，对应5个打印日志的函数
logging.info('the logging module is working.')
logging.warning('an error message is about to be logged.')
logging.error('an error has occurred.')
logging.critical('the program is unable to recover!')



import logging
import logging.config

def main():
    logging.config.fileConfig('logconfig.ini') #从磁盘文件中读取日志的配置选项

    hostname='www.python.org'
    item='spam'
    filename='data.csv'
    mode='r'
    logging.critical('host {} unknown'.format(hostname))
    logging.error('could not find {!r}'.format(item))
    logging.warning('feature is deprecated')
    logging.info('opening file {!r}, mode={!r}'.format(filename, mode))
    logging.debug('got here')

if __name__=="__main__":
    main()



import logging
log=logging.getLogger(__name__)
log.addHandler(logging.NullHandler())

def func():
    log.critical('a critical error!')
    log.debug('a debug message')
