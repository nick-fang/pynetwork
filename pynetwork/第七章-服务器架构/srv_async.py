"""代码清单7-6 使用select模块构造异步服务器；Windows下无法运行此脚本"""
import socket
import select
import zen_utils

def serve(listener):
    sockets = {listener.fileno():listener} #用监听套接字的文件描述符作为字典的键
    addresses = {}
    bytes_received = {}
    bytes_to_send = {}
    
    poll_object = select.poll() #注意：Windows系统只支持select.select()
    poll_object.register(listener, select.POLLIN) #向poll对象注册listener监听套接字，以监视它的【POLLIN事件】

    while True: #事件监视循环
        for fd, event in poll_object.poll(): #fd是文件描述符，event是事件掩码；poll()类似selectors模块的sel.select()方法
            sock = sockets[fd] #先从sockets字典中获得sock套接字对象

            if event & (select.POLLHUP | select.POLLERR | select.POLLNVAL):
                address = addresses.pop(sock) #从字典中弹出sock键，返回sock键对应的值
                rb = bytes_received.pop(sock, b'')
                sb = bytes_to_send.pop(sock, b'')
                if rb:
                    print('client {} sent {} but then closed'.format(address, rb))
                elif sb:
                    print('client {} closed before we sent {}'.format(address, sb))
                else:
                    print('client {} closed socket normally'.format(address))
                poll_object.unregister(fd)
                del sockets[fd]

            elif sock is listener: #这段elif块结束后，会不会直接执行下面的select.POLLIN块？？因为监听套接字注册的事件就是“select.POLLIN”？？但是监听套接字是无法使用下面的sock.recv()方法的？？
                sock, address = sock.accept() #把左边的sock改成conn，以避免歧义？？
                print('accepted connection from {}'.format(address))
                sock.setblocking(False)
                sockets[sock.fileno()] = sock #将连接套接字添加进sockets字典中
                addresses[sock] = address #将连接套接字的远端地址添加进address字典中
                poll_object.register(sock, select.POLLIN) #向poll对象注册sock连接套接字，以监视它的【POLLIN事件】

            elif event & select.POLLIN:
                more_data = sock.recv(4096)
                if not more_data:
                    sock.close()
                    continue
                data = bytes_received.pop(sock, b'') + more_data
                if data.endswith(b'?'):
                    bytes_to_send[sock] = zen_utils.get_answer(data)
                    poll_object.modify(sock, select.POLLOUT)
                else:
                    bytes_received[sock] = data

            elif event & select.POLLOUT:
                data = bytes_to_send.pop(sock)
                n = sock.send(data)
                if n < len(data):
                    bytes_to_send[sock] = data[n:]
                else:
                    poll_object.modify(sock, select.POLLIN)

if __name__ == "__main__":
    address = zen_utils.parse_command_line('low-level async server')
    listener = zen_utils.create_srv_socket(address) #创建并返回一个绑定在指定addr上的监听套接字
    serve(listener)
