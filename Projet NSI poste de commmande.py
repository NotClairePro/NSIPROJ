import socket

#================================= Connection Raspberry ====================================#

HOST = '' # Enter IP or Hostname of your server # A completer
PORT = 12345 # Pick an open Port (1000+ recommended), must match the server port
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.connect((HOST,PORT))

#Lets loop awaiting for your input
while True:
	command = raw_input('Enter your command: ')
	s.send(command)
	#reply = s.recv(1024)


#===================================== Fonction general ====================================#
def Convertion_180(nbr): #Convertisseur de rappot -1/0/1 a 0/85/180 a mettre sur la station de controle
    N_nbr = 0
    if nbr == -1:
        N_nbr = 0
    elif nbr < 0:
        N_nbr = abs(nbr*85)
    elif nbr == 0:
        N_nbr = 85
    elif nbr > 0:
        N_nbr = (nbr*85)+95
    elif nbr == 1:
        N_nbr = 180
    else :
        raise ValueError
    return round(N_nbr)

  
  # + le code Claire avec la definition des ID_Controls
