import cv2
import socket
import pickle
from circle_detect import circle_centre


import select
import queue


# Define Socket Interface
server_ip = '192.168.0.57'
server_port = 5000

server_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
server_socket.bind((server_ip, server_port))
print(f"\nServer socket created and bound to IP addr: '{server_ip}' on port {server_port}\n")


def send_to_client(client_ip, client_port, message):
    message = bytes(message, 'utf-8')
    recv_port = client_port+10
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as quick_socket:
        quick_socket.connect((client_ip, recv_port))
        quick_socket.send(message)


# Initialize position variables
prev_x, prev_y = 0, 0
circle_detected = False

# Process image
while True:
    data = server_socket.recvfrom(1000000)
    # server_socket.setblocking(False)

    client_ip, client_port = data[1]  # This is a tuple
    input_bytes = data[0]

    # print(client_ip, client_port)

    # Image processing
    footage = pickle.loads(input_bytes)
    footage = cv2.imdecode(footage, cv2.IMREAD_COLOR)
    footage_circ_detected, curr_x, curr_y = circle_centre(footage)

    try:
        dx = curr_x - prev_x
        dy = curr_y - prev_y
        update = f'dx = {dx}, dy = {dy}'
        send_to_client(client_ip, client_port, update)
        prev_x, prev_y = curr_x, curr_y # updates values detected
        circle_detected = True # updates that circle is detected
    except TypeError:  # Corrects for None output
        if circle_detected:
            update = 'No circle detected'
            send_to_client(client_ip, client_port, update)
            circle_detected = False
    
    cv2.imshow('footage', footage)
    cv2.imshow('footage', footage_circ_detected)
    cv2.waitKey(25)
    
