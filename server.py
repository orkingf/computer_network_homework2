import socket
import threading

# 保存所有客户端连接的列表
clients = []

# 发送消息给所有客户端的函数
def broadcast(message, client_socket=None):
    for client in clients:
        if client != client_socket:  # 不回发给发送者自己
            try:
                client.send(message)  # 尝试发送消息
            except:
                clients.remove(client)  # 如果发送失败，从客户端列表中移除该客户端

# 用户验证
def validate_credentials(username, password):
    # 简单的用户名和密码验证，实际应用中应该检查数据库
    # 这里用的是硬编码的验证，仅作为示例
    valid_users = {
        "admin": "password123",  # 示例用户名及密码
        "user": "pass"
    }
    if username in valid_users and valid_users[username] == password:
        return True
    return False

#处理客户端信息
def handle_client(client_socket, client_address):
    print(f"New connection from {client_address}")  # 打印新连接的客户端地址
    try:
        # 接收用户名和密码
        credentials = client_socket.recv(1024).decode()  # 格式应为 "username,password"
        username, password = credentials.split(',')
        if validate_credentials(username, password):
            client_socket.send(b"Login successful\n")  # 发送登录成功消息
            print(f"User {username} logged in successfully")
            # 可以继续进行消息接收和发送操作或者其他逻辑
        else:
            client_socket.send(b"Login failed\n")  # 发送登录失败消息
            client_socket.close()  # 关闭连接
            return
    except Exception as e:
        print(f"Error during login: {e}")
        client_socket.close()  # 出错时关闭连接
        return

    # 用户登录成功后，继续接收消息
    while True:
        try:
            message = client_socket.recv(1024)
            if message:
                print(f"Received message from {client_address}: {message.decode()}")
                broadcast(message, client_socket)  # 调用广播函数发送消息给所有其他客户端
            else:
                # 没有消息意味着客户端断开连接
                break
        except:
            break
    # 清理工作
    clients.remove(client_socket)
    client_socket.close()
    print(f"Connection closed for {client_address}")


# 服务器主函数
def start_server(host='0.0.0.0', port=12345):
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)  # 创建TCP服务器socket
    server_socket.bind((host, port))  # 绑定到指定的host和port上
    server_socket.listen()  # 开始监听
    print(f"Server is listening on {host}:{port}")

    while True:
        client_socket, client_address = server_socket.accept()  # 接受新的客户端连接
        clients.append(client_socket)  # 将客户端socket添加到客户端列表
        thread = threading.Thread(target=handle_client, args=(client_socket, client_address))  # 为每个客户端创建一个新的线程
        thread.start()  # 启动线程

# 主程序入口
if __name__ == "__main__":
    start_server()