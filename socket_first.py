from socket import socket, AF_INET, SOCK_STREAM
from threading import Thread

__author__ = 'cln'

port = 50008
host = 'localhost'


def server():
    # 建立tcp连接
    sock = socket(AF_INET, SOCK_STREAM)
    # 绑定本机和端口
    sock.bind(('', port))
    # 监听，允许连接的客户数量
    sock.listen(5)
    while True:
        # 等待客户端连接
        conn, addr = sock.accept()
        # 读取客户端请求的字节数据
        data = conn.recv(1024)
        # 响应请求给客户端
        reply = 'server got [%s]' % data
        conn.send(reply.encode())


def client(name):
    sock = socket(AF_INET, SOCK_STREAM)
    sock.connect((host, port))
    sock.send(name.encode())
    reply = sock.recv(1024)
    sock.close()
    print('client got [%s]' % reply)


if __name__ == '__main__':
    sthread = Thread(target=server)
    sthread.daemon = True
    sthread.start()
    for i in range(5):
        Thread(target=client, args=('client%s' % i, )).start()