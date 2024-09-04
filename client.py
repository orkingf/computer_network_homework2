import socket
import threading

# 处理接收消息的线程
def receive_messages(client_socket):
    while True:
        try:
            message = client_socket.recv(1024)
            if message:
                print(f"From server: {message.decode()}")
            else:
                break
        except:
            break

# 客户端主函数
def start_client(host='101.200.86.88', port=12345):
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client_socket.connect((host, port))

    receive_thread = threading.Thread(target=receive_messages, args=(client_socket,))
    receive_thread.start()

    while True:
        message = input()
        if message.lower() == "exit":
            client_socket.close()
            break
        client_socket.send(message.encode())

# 主程序入口
if __name__ == "__main__":
    start_client()
