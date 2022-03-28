import socket

HOST = "127.0.0.1"  # The server's hostname or IP address
PORT = 45554  # The port used by the server

serv = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
serv.connect((HOST, PORT))
print("Connection on {}".format(PORT))

from Ctrls import Strt, Controls

if __name__ == '__main__':
    Manette = Controls()
    mode = 0
    while True:
        Strt(Manette)
        if mode == 0: #bouger
            func = "bougerListeServo"

            if Manette.JL != [0,0]: #servo 0 et servo 2 = bras gauche
                angles = JL
                server.send("[func,[0,2], angles]".encode('UTF-8'))

            if Manette.JR != [0,0]: #servo 0 et servo 2 = bras gauche
                angles = JR

                server.send("[func,[5,7], angles]".encode('UTF-8'))

        else: #setPosition
            print("boop"
