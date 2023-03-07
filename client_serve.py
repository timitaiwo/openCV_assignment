import socket
from client_stream import client_ip, client_port

recv_port = client_port+10

client_recv_sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client_recv_sock.bind((client_ip, recv_port))
print(f'\nsocket created and bound to {client_ip} on port {recv_port}')

client_recv_sock.listen()
# print(f'\nConnected to {conn_ip} on {conn_port}')

while True:
    conn, (conn_ip, conn_port) = client_recv_sock.accept()
    data = conn.recv(1024)
    data = bytes.decode(data)
    print(data, '\n')
