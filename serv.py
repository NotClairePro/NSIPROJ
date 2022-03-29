# Echo server program
import socket
import time
HOST = 'localhost'
PORT = 45554
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.bind((HOST, PORT))
s.listen(1)

conn, addr = s.accept()
print('Connected by', addr)

while 1:
	data = conn.recv(1024)
	data = data.decode("utf-8")
	if data:
		print(f"{data} \n")
conn.close()