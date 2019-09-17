"""
ftp 文件服务 ，客户端
"""
from socket import *
import sys
from time import sleep

# 服务器地址
ADDR = ('176.28.11.75',6666)

# 具体功能实现
class FtpClient:
    """
    实现具体功能请求
    """
    def __init__(self,sockfd):
        self.sockfd = sockfd

    # 获取文件列表
    def do_list(self):
        self.sockfd.send(b'L') # 发送请求
        # 等待回去，确认是否有文件列表
        data = self.sockfd.recv(128).decode()
        if data == 'OK':
            data = self.sockfd.recv(1024 * 1024).decode()
            print(data)

            # while True:
            #     data = self.sockfd.recv(128).decode()
            #     if data == '##':
            #         break
            #     print(data)
        else:
            print(data) # 不可以查看的原因

    # 退出
    def do_quit(self):
        self.sockfd.send(b'Q')
        self.sockfd.close()
        sys.exit("谢谢使用")

    def do_get(self,filename):
        # 发送请求
        self.sockfd.send(('G '+filename).encode())
        # 等待回复
        data = self.sockfd.recv(128).decode()
        # 接收文件
        if data == 'OK':
            f = open(filename,'wb')
            # 循环接收内容，写入文件
            while True:
                data = self.sockfd.recv(1024)
                if data == b'##':
                    break
                f.write(data)
            f.close()
        else:
            print(data)

    def do_put(self,filename):
        try:
            f = open(filename,'rb')
        except Exception:
            print("文件不存在")
            return
        # 获取真正的文件名
        filename = filename.split('/')[-1]
        # 发送请求
        self.sockfd.send(('P '+filename).encode())
        # 等待回复
        data = self.sockfd.recv(128).decode()
        if data == 'OK':
            while True:
                data = f.read(1024)
                if not data:
                    sleep(0.1)
                    self.sockfd.send(b'##')
                    break
                self.sockfd.send(data)
            f.close()
        else:
            print(data)

# 网络大家，和终端输入命令选项
def main():
    sockfd = socket()
    try:
        sockfd.connect(ADDR)
    except Exception as e:
        print(e)
        return

    # 实例化对象
    ftp = FtpClient(sockfd)

    # 循环发起请求
    while True:
        print("\n=========Command==============")
        print("*****       list        *****")
        print("*****     get  file     *****")
        print("*****     put  file     *****")
        print("*****       quit        *****")
        print("===============================")
        cmd = input("Command:")
        if cmd.strip() == 'list':
            ftp.do_list()
        elif cmd.strip() == 'quit':
            ftp.do_quit()
        elif cmd[:3] == 'get':
            filename = cmd.split(' ')[-1]
            ftp.do_get(filename)
        elif cmd[:3] == 'put':
            filename = cmd.split(' ')[-1]
            ftp.do_put(filename)
        else:
            print("请输入正确命令!")

if __name__ == '__main__':
    main()