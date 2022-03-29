# Echo server program
import socket
HOST = 'localhost'
PORT = 45554
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# managing error exception
s.bind((HOST, PORT))
s.listen(1)

conn, addr = s.accept()
print('Connected by', addr)
lservo = [85, 85, 85, 85, 85, 85, 85, 85, 85, 85, 85, 85]
while True:
	data = conn.recv(1024)
	if data:
		N_data = data.decode('utf-8')

		if N_data == 'terminate':
			conn.close()
			break
		if N_data == "getPos":
			conn.send(f"{lservo}".encode('utf-8'))
			continue
		liste = eval(N_data)
		if liste[0] == 'bougerListeServo':
			print(liste)
