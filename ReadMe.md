#Image processing and networking in Python using the OpenCV and socket libraries

The aim of this project is to detect a red circle against a white background. The image is captured on one computer and streamed via a UDP socket to a second computer which processes it and gets the location of the circle's centre. The second computer then sends this information as a message back via a TCP socket to the first computer which displays it on it's terminal.
