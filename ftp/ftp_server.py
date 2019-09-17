from socket import *
import os,sys
from threading import Thread
from time import sleep

#  思想 ：将套接字的创建份封装成一个函数
#  将


#自定义线程类
class FtpServer(Thread):
    def __init__(self,connfd):
        self.connfd=connfd
        self.filename="/home/tarena/"
        super().__init__()







    #
    def run(self):
        date=self.connfd
        if date[0]=="L":
            pass

# 构建网络模型
def main():
#创建套接字
    sockfd=socket()
    sockfd.setsockopt(SOL_SOCKET,SO_REUSEADDR,1)
    server_addr=("0.0.0.0",8888)
    sockfd.bind(server_addr)
    # 监听
    sockfd.listen(5)

    #循环接收消息
    while True:
        #判断接收消息数据
        try:
            connfd,addr=sockfd.accept()
            print("From ",addr)
        except KeyboardInterrupt as e:
            print("Server Ever")
            os._exit(0)
        except Exception as e:
            print(e)
            continue

        #将套接字 变成一个对象 传给 服务器类
        t=FtpServer(connfd)
        t.setDaemon(True)
        t.start()





