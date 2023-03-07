import cv2
import socket
import pickle

# Define Socket interface
client_ip = '192.168.0.13'
client_port = 6000

server_ip = '192.168.0.57'
server_port = 5000


def capture_and_send(webcam):
    '''
    Capture image from webcam and send to server
    '''

    with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as client_send_sock:
        client_send_sock.bind((client_ip, client_port))
        client_send_sock.setsockopt(socket.SOL_SOCKET, socket.SO_SNDBUF, 1000000)

        while webcam.isOpened():
            _, footage = webcam.read()
            cv2.imshow('captured image', footage)
            
            # Encode image for tranmission
            _, footage = cv2.imencode('.jpg', footage, [int(cv2.IMWRITE_JPEG_QUALITY), 30])
            footage_as_bytes = pickle.dumps(footage)

            # Transmit data
            client_send_sock.sendto((footage_as_bytes), (server_ip, server_port))
            
            cv2.waitKey(25)


if __name__ == '__main__':

    # Define webcam
    webcam = cv2.VideoCapture(2) # Laptop Version
    # webcam = cv2.VideoCapture(0) # RasPi Version

    capture_and_send(webcam)