import socket
import time
from Ctrls import Strt, Controls

HOST = "127.0.0.1"  # The server's hostname or IP address
PORT = 45554  # The port used by the server

serv = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
serv.connect((HOST, PORT))
print("Connection on {}".format(PORT))

if __name__ == '__main__':
    Manette = Controls()

    mode = 0
    servChoisi = 0
    Partie = 0
    while True:
        Strt(Manette)
        if Manette.Menu:
            if Manette.T:
                mode = 1
            elif Manette.X:
                mode = 0

        if mode == 0:  # bouger
            func = "bougerListeServo"
            if Manette.L1:
                # On est dans le mode de Choix du servChoisi a bouger:
                if Manette.T:
                    servChoisi = 1
                elif Manette.R:
                    servChoisi = 2
                elif Manette.X:
                    servChoisi = 3
                elif Manette.C:
                    servChoisi = 4
                elif Manette.Up:
                    servChoisi = 5
                elif Manette.Down:
                    servChoisi = 6
                elif Manette.Left:
                    servChoisi = 7
                elif Manette.Right:
                    servChoisi = 8
                elif Manette.LSB:
                    servChoisi = 9
                elif Manette.RSB:
                    servChoisi = 10
                elif Manette.Share:
                    servChoisi = 11
                elif Manette.Opt:
                    servChoisi = 12
                print(f"serv choisi: {servChoisi}")
            if Manette.R1:
                if Manette.Up:
                    time.sleep(0.5)
                    serv.send(f"{[func, [servChoisi - 1], [5]]}".encode('UTF-8'))
                elif Manette.Down:
                    time.sleep(0.5)
                    serv.send(f"{[func, [servChoisi - 1], [-5]]}".encode('UTF-8'))
                elif Manette.Left:
                    time.sleep(0.5)
                    serv.send(f"{[func, [servChoisi - 1], [5]]}".encode('UTF-8'))
                elif Manette.Right:
                    time.sleep(0.5)
                    serv.send(f"{[func, [servChoisi - 1], [-5]]}".encode('UTF-8'))
            # On n'est pas dans le mode de controle de servChoisi individuel
            else:

                if Manette.JL != [0, 0]:  # servChoisi 0 et servChoisi 2 = bras gauche
                    angles = Manette.JL
                    time.sleep(0.5)
                    serv.send(f"{[func, [0, 2], angles]}".encode('UTF-8'))

                if Manette.JR != [0, 0]:  # servChoisi 0 et servChoisi 2 = bras gauche
                    angles = Manette.JR
                    time.sleep(0.5)
                    serv.send(f"{[func, [5, 7], angles]}".encode('UTF-8'))

                if Manette.Up:
                    time.sleep(0.5)
                    serv.send(f"{[func, [10], [5]]}".encode('UTF-8'))
                elif Manette.Down:
                    time.sleep(0.5)
                    serv.send(f"{[func, [10], [-5]]}".encode('UTF-8'))
                elif Manette.Left:
                    time.sleep(0.5)
                    serv.send(f"{[func, [11], [5]]}".encode('UTF-8'))
                elif Manette.Right:
                    time.sleep(0.5)
                    serv.send(f"{[func, [11], [-5]]}".encode('UTF-8'))
        else:  # setPosition
            print("boop")
            func = "setPosition"
