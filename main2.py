import socket
import time
from Ctrls import Strt, Controls

HOST = "127.0.0.1"  # The server's hostname or IP address
PORT = 45554  # The port used by the server

serv = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
serv.connect((HOST, PORT))
print("Connection on {}".format(PORT))
with open("positions.txt", "r") as f:
    positions = f.readlines()
    for i in range(len(positions)):
        positions[i] = positions[i].rstrip('\n')
    dictPositions = {}
    for i in range(len(positions)):
        rupt = positions[i].index(":")
        dictPositions[positions[i][:rupt]] = eval(positions[i][rupt + 1:])

for key, val in dictPositions.items():
    print(key, val)
del positions
Names = [key for key in dictPositions.keys()]

if __name__ == '__main__':

    Manette = Controls()
    CurrentPos = 0
    servChoisi = 0
    func = "bougerListeServo"
    while True:
        Strt(Manette)
        if Manette.L1 and Manette.R1 and Manette.L2 and Manette.R2:
            serv.send("terminate".encode("UTF-8"))

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

        elif Manette.R1:
            if Manette.Up:
                serv.send(f"{[func, [servChoisi - 1], [5]]}".encode('UTF-8'))
                time.sleep(0.5)
            elif Manette.Down:
                serv.send(f"{[func, [servChoisi - 1], [-5]]}".encode('UTF-8'))
                time.sleep(0.5)
            elif Manette.Left:
                serv.send(f"{[func, [servChoisi - 1], [5]]}".encode('UTF-8'))
                time.sleep(0.5)
            elif Manette.Right:
                serv.send(f"{[func, [servChoisi - 1], [-5]]}".encode('UTF-8'))
                time.sleep(0.5)
        # On n'est pas dans le mode de controle de servo individuel
        elif Manette.L2 and Manette.R2:

                if Manette.Up:
                    CurrentPos = CurrentPos + (CurrentPos+1 < len(Names))
                if Manette.Down:
                    CurrentPos = CurrentPos - (CurrentPos > 0)
                if Manette.R:  # ajouter la pos dans dictPositions
                    serv.send(f"getPos".encode('UTF-8'))
                    time.sleep(0.5)
                    data = serv.recv(1024)
                    data = data.decode('UTF-8')
                    data = eval(data)
                    Names.append(input("Nom de la position: \n"))
                    dictPositions[Names[-1]] = data
                    with open("positions.txt", "w+") as f:
                        for key, val in dictPositions.items():
                            f.write(f"{key}:{val}\n")
                    print(f"new pos added: {Names[-1]}")
                if Manette.Opt and Manette.Share:  # supprimer la pos dans dictPositions, Names et du fichier

                    with open("positions.txt", "w+") as f:
                        for key, val in dictPositions.items():
                            if val == CurrentPos:
                                Names.remove(key)
                                dictPositions.pop(key)
                                print(f"pos deleted: {key}")
                            else:
                                f.write(f"{key}:{val}\n")
        else:

            if Manette.JL != [0, 0]:  # servChoisi 0 et servChoisi 2 = bras gauche
                angles = Manette.JL
                serv.send(f"{[func, [0, 2], angles]}".encode('UTF-8'))
                time.sleep(0.5)
            if Manette.JR != [0, 0]:  # servChoisi 0 et servChoisi 2 = bras gauche
                angles = Manette.JR
                serv.send(f"{[func, [5, 7], angles]}".encode('UTF-8'))
                time.sleep(0.5)
            if Manette.Up:
                serv.send(f"{[func, [10], [5]]}".encode('UTF-8'))
                time.sleep(0.5)
            elif Manette.Down:
                serv.send(f"{[func, [10], [-5]]}".encode('UTF-8'))
                time.sleep(0.5)
            elif Manette.Left:
                serv.send(f"{[func, [11], [5]]}".encode('UTF-8'))
                time.sleep(0.5)
            elif Manette.Right:
                serv.send(f"{[func, [11], [-5]]}".encode('UTF-8'))
                time.sleep(0.5)


