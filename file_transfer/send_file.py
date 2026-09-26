def send_file(filename: str = "mytext.txt", testing: bool = False) -> None:
    import socket

    port = 12312  # 为服务预留端口
    sock = socket.socket()  # 创建套接字对象
    host = socket.gethostname()  # 获取本地主机名
    sock.bind((host, port))  # 绑定到端口
    sock.listen(5)  # 等待客户端连接

    print("Server listening....")

    while True:
        conn, addr = sock.accept()  # 与客户端建立连接
        print(f"Got connection from {addr}")
        data = conn.recv(1024)
        print(f"Server received: {data = }")

        with open(filename, "rb") as in_file:
            data = in_file.read(1024)
            while data:
                conn.send(data)
                print(f"Sent {data!r}")
                data = in_file.read(1024)

        print("Done sending")
        conn.close()
        if testing:  # 允许测试结束
            break

    sock.shutdown(1)
    sock.close()


if __name__ == "__main__":
    send_file()
