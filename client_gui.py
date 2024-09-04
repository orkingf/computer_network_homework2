import socket
import threading
import tkinter as tk
from tkinter import scrolledtext, filedialog, messagebox

#创建套接字
host = '101.200.86.88'
port = 12345
client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client_socket.connect((host, port))

#从服务器接受信息
def receive_messages(client_socket, text_area):
    while True:
        try:
            message = client_socket.recv(1024)
            if message:
                text_area.config(state=tk.NORMAL)  # Enable editing
                text_area.insert(tk.END, f"From server: {message.decode()}\n")
                text_area.config(state=tk.DISABLED)  # Disable editing
                text_area.yview(tk.END)  # Auto-scroll to the end
            else:
                break
        except:
            break

#传输文件到服务器
def send_file(client_socket):
    filepath = filedialog.askopenfilename()
    if filepath:
        with open(filepath, 'r',encoding='utf-8') as f:
            contents = f.read()
            client_socket.send(contents.encode())


def receive_complete_message(socket):
    buffer = ""
    while not buffer.endswith("\n"):
        data = socket.recv(1024).decode()
        if not data:
            break
        buffer += data
    return buffer.strip()
# 客户端主函数
def start_client(client_socket):


    # 设置GUI
    root = tk.Tk()
    root.title("Chat Client")

    # 发送消息到服务器
    def send_message(entry_widget, client_socket):
        message = entry_widget.get()
        if message == 'exit':
            client_socket.send(message.encode())
            client_socket.close()
            root.quit()
            root.destroy()
        else:
            client_socket.send(message.encode())
            entry_widget.delete(0, tk.END)

    # 文本显示区域
    text_area = scrolledtext.ScrolledText(root, state='disabled', width=40, height=10)
    text_area.grid(row=0, column=0, columnspan=2, padx=20, pady=20)

    # 消息输入框
    msg_entry = tk.Entry(root, width=30)
    msg_entry.grid(row=1, column=0, pady=10, padx=10)

    # 发送按钮
    send_button = tk.Button(root, text="Send", command=lambda: send_message(msg_entry, client_socket))
    send_button.grid(row=1, column=1, pady=10, padx=10)

    # 发送文件按钮
    send_button = tk.Button(root, text="Send file",command=lambda: send_file(client_socket))
    send_button.grid(row=2, column=1, pady=10, padx=10)

    # 开启接收消息的线程
    receive_thread = threading.Thread(target=receive_messages, args=(client_socket, text_area))
    receive_thread.start()

    # 启动GUI主循环
    root.mainloop()




# 用户登录
def login():
    # 设置登录GUI
    log_face = tk.Tk()
    log_face.title("Login")

    # 用户名输入
    tk.Label(log_face, text="Username:").grid(row=0, column=0, pady=10, padx=10)
    username_entry = tk.Entry(log_face, width=30)
    username_entry.grid(row=0, column=1, pady=10, padx=10)

    # 密码输入
    tk.Label(log_face, text="Password:").grid(row=1, column=0, pady=10, padx=10)
    password_entry = tk.Entry(log_face, width=30, show='*')
    password_entry.grid(row=1, column=1, pady=10, padx=10)

    # 登录按钮
    login_button = tk.Button(log_face, text="Login", command=lambda: try_login(username_entry, password_entry, log_face))
    login_button.grid(row=2, column=0, columnspan=2, pady=10, padx=10)

    log_face.mainloop()

def try_login(username_entry, password_entry, log_face):
    username = username_entry.get()
    password = password_entry.get()
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    try:
        client_socket.connect((host, port))
        # 发送用户名和密码，待验证逻辑
        client_socket.send(f"{username},{password}".encode())
        # 接收验证结果
        response = receive_complete_message(client_socket)
        if response == "Login successful":
            messagebox.showinfo("Login Info", "Login Successful!")
            log_face.destroy()
            start_client(client_socket)
        else:
            messagebox.showerror("Login Info", "Login Failed, please try again.")
    except Exception as e:
        messagebox.showerror("Login Info", str(e))
        
# 主程序入口
if __name__ == "__main__":
    login()