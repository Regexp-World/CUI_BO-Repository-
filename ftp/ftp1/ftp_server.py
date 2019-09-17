"""
ftp 文件服务器 服务端
多进程/多线程并发 socket
"""
from socket import *
from threading import Thread
import sys,os
from time import sleep

HOST = '176.28.11.75'
PORT = 6666
ADDR = (HOST,PORT)
FTP = "/home/tarena/FTP/" # 文件库位置

# 实现具体功能
class FtpServer(Thread):
    """
    查看文件列表，上传，下载，退出
    """
    def __init__(self,connfd):
        self.connfd = connfd
        super().__init__()

    def do_list(self):
        files = os.listdir(FTP)
        if not files:
            self.connfd.send("充值VIP,百万图书任你选".encode())
            return
        else:
            self.connfd.send(b'OK')
            sleep(0.1)

        filelist = ""
        for file in files:
            if file[0] != '.' and \
                    os.path.isfile(FTP+file):
                filelist += file + '\n'
        self.connfd.send(filelist.encode())

        # for file in files:
        #     # 不是隐藏文件并且是普通文件
        #     if file[0] != '.' and \
        #             os.path.isfile(FTP+file):
        #         sleep(0.1)
        #         self.connfd.send(file.encode())
        # sleep(0.1)
        # self.connfd.send(b'##')

    # 下载文件
    def do_get(self,filename):
        try:
            f = open(FTP+filename,'rb')
        except Exception:
            # 文件不存在
            self.connfd.send("vip可以下载".encode())
            return
        else:
            self.connfd.send(b'OK')
            sleep(0.1)
        # 发送文件
        while True:
            data = f.read(1024)
            if not data:
                sleep(0.1)
                self.connfd.send(b'##')
                break
            self.connfd.send(data)
        f.close()

    # 上传
    def do_put(self,filename):
        if os.path.exists(FTP+filename):
            self.connfd.send('文件已存在'.encode())
            return
        else:
            self.connfd.send(b'OK')
        # 接收文件
        f = open(FTP+filename,'wb')
        while True:
            data = self.connfd.recv(1024)
            if data == b'##':
                break
            f.write(data)
        f.close()

    # 分配任务
    def run(self):
        while True:
            # 客户端请求
            data=self.connfd.recv(1024).decode()
            # 判断请求类型
            if not data or data == 'Q':
                return # 线程结束
            elif data == 'L':
                self.do_list()
            elif data[0] == 'G':
                filename = data.split(' ')[-1]
                self.do_get(filename)
            elif data[0] == 'P':
                filename = data.split(' ')[-1]
                self.do_put(filename)

# 搭建网络并发模型
def main():
    # 创建套接字
    s = socket()
    s.setsockopt(SOL_SOCKET, SO_REUSEADDR, 1)
    s.bind(ADDR)
    s.listen(5)

    print("Listen the port 8888...")
    while True:
        # 循环等待客户端连接
        try:
            c, addr = s.accept()
            print("Connect from", addr)
        except KeyboardInterrupt as e:
            sys.exit("服务器退出")
        except Exception as e:
            print(e)
            continue

        # 创建线程
        t = FtpServer(c)
        t.setDaemon(True)
        t.start()

if __name__ == '__main__':
   main()