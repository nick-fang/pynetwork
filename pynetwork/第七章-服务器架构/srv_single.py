"""代码清单7-3 最简单的单线程服务器"""
import zen_utils

if __name__ == "__main__":
    address = zen_utils.parse_command_line('simple single-threaded server') #解析命令行参数，获取address
    listener = zen_utils.create_srv_socket(address) #创建【监听套接字】
    zen_utils.accept_connections_forever(listener) #监听循环：不断监听来自客户端的连接请求，并据此创建【连接套接字】
