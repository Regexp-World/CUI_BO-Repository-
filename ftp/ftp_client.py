from socket import *
import os,sys
# 构建网络模型
# 创建套接字,创建连接地址
# 全局变量 连接地址
HOST=8888
addr="0.0.0.0"
ADDR=(addr,HOST)

class FtpClient:
    def __init__(self,connfd):
        self.connfd=connfd

    def list(self):
        self.connfd.send("L".encode())

    def getlist(self):
        pass

    def putlist(self):
        pass

    def quit(self):
        pass







# 构建网络模型
#服务器只用构建 两个模块
# 控制打印输出 和具体的方法类
def main():
    sockfd=socket()
    #创建套接字 并连接到服务器
    try:
        sockfd.connect(ADDR)

    except Exception as  e:
        print(e)

    #注意 该地方巧妙之处
    #如果我想要通过一个类操作上面函数的变量
    #这时可以直接把上面的变量当做参数 传给创建的类
    #在类里面进行函数的构建,这样从而达到操作变量的目的
    #最后通过类调用方法
    f=FtpClient(sockfd)


    #创建
    while True:
        print("\n=========Command==============")
        print("*****       list        *****")
        print("*****     get  file     *****")
        print("*****     put  file     *****")
        print("*****       quit        *****")
        print("===============================")
        cmd=input("请输入操作指令!")
        if cmd=="":
            print("Error")

        #根据操作指令 判断
        elif cmd.strip(" ")=="list":
            f.list()
        elif cmd.strip(" ")=="G":
            f.getlist()
        elif cmd.strip(" ")=="P":
            f.putlist()
        elif cmd.strip(" ")=="Q":
            f.quit()


if __name__ == '__main__':
    main()