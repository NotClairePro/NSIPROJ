import socket
import time
from Ctrls import Strt, Controls

HOST = "192.168.1.61"  # The server's hostname or IP address
PORT = 12345  # The port used by the server

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
    onpeu = True
    while True:
        Strt(Manette)
        if onpeu is False:
            dat = serv.recv(1024)
            if dat:
                if dat.decode('utf-8') == "done":
                    onpeu = True
            continue
        if Manette.L1 and Manette.R1 and Manette.L2 and Manette.R2:
            serv.send("terminate".encode("UTF-8"))
            break
        elif Manette.R2 > 0.3 and Manette.L2 > 0.3:
            Up = Manette.Up
            serv.send(
                f"{['avancer', [0, 1, 2, 3, 4, 5], [int(Manette.R2 * 255), True * Up , True* (not Up), int(Manette.L2 * 255), True * Up , True* (not Up)]]}".encode(
                    'UTF-8'))
            onpeu = False
            continue
        elif Manette.R2 > 0.3:
            Up = Manette.Up
            serv.send(
                f"{['avancer', [0, 1, 2], [int(Manette.R2 * 255), True * Up , True* (not Up)]]}".encode(
                    'UTF-8'))
            onpeu = False
            continue
        elif Manette.R2 > 0.3:
            Up = Manette.Up
            serv.send(
                f"{['avancer', [3, 4, 5], [int(Manette.L2 * 255), True * Up , True* (not Up)]]}".encode(
                    'UTF-8'))
            onpeu = False
            continue

        elif Manette.L1:
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
            continue
        elif Manette.R1:
            if Manette.Up:
                serv.send(f"{[func, [servChoisi - 1], [5]]}".encode('UTF-8'))
                onpeu = False
            elif Manette.Down:
                serv.send(f"{[func, [servChoisi - 1], [-5]]}".encode('UTF-8'))
                onpeu = False
            elif Manette.Left:
                serv.send(f"{[func, [servChoisi - 1], [5]]}".encode('UTF-8'))
                onpeu = False
            elif Manette.Right:
                serv.send(f"{[func, [servChoisi - 1], [-5]]}".encode('UTF-8'))
                onpeu = False
            continue
        # On n'est pas dans le mode de controle de servo individuel
        elif Manette.RSB and Manette.LSB:
            if Manette.Menu:
                serv.send(f"{[func, [o for o in range(12)], dictPositions[Names[CurrentPos]]]}".encode('UTF-8'))
                onpeu = False
            elif Manette.Up:
                CurrentPos = CurrentPos + (CurrentPos + 1 < len(Names))
            elif Manette.Down:
                CurrentPos = CurrentPos - (CurrentPos > 0)
            elif Manette.R:  # ajouter la pos dans dictPositions
                serv.send(f"getPos".encode('UTF-8'))
                time.sleep(1)
                data = serv.recv(1024)
                data = data.decode('UTF-8')
                data = eval(data)
                data = [int(elem) for elem in data]
                Names.append(input("Nom de la position: \n"))
                dictPositions[Names[-1]] = data
                with open("positions.txt", "w+") as f:
                    for key, val in dictPositions.items():
                        f.write(f"{key}:{val}\n")
                print(f"new pos added: {Names[-1]}")
            elif Manette.Opt and Manette.Share:  # supprimer la pos dans dictPositions, Names et du fichier

                with open("positions.txt", "w+") as f:
                    for key, val in dictPositions.items():
                        if val == CurrentPos:
                            Names.remove(key)
                            dictPositions.pop(key)
                            print(f"pos deleted: {key}")
                        else:
                            f.write(f"{key}:{val}\n")
            continue



        else:

            if Manette.JL != [0, 0]:  # servChoisi 0 et servChoisi 2 = bras gauche
                angles = Manette.JL
                for k in range(len(angles)):
                    if angles[k] > 1:
                        angles[k] = 1
                    elif angles[k] < -1:
                        angles[k] = -1
                serv.send(f"{[func, [0, 2], [angles[1], angles[0]]]}".encode('UTF-8'))
                onpeu = False
            elif Manette.JR != [0, 0]:  # servChoisi 0 et servChoisi 2 = bras gauche
                angles = Manette.JR
                for k in range(len(angles)):
                    if angles[k] > 1:
                        angles[k] = 1
                    elif angles[k] < -1:
                        angles[k] = -1

                serv.send(f"{[func, [5, 7], angles]}".encode('UTF-8'))
                onpeu = False
            elif Manette.Up:
                serv.send(f"{[func, [10], [0.5]]}".encode('UTF-8'))
                onpeu = False
            elif Manette.Down:
                serv.send(f"{[func, [10], [-0.5]]}".encode('UTF-8'))
                onpeu = False
            elif Manette.Left:
                serv.send(f"{[func, [11], [0.5]]}".encode('UTF-8'))
                onpeu = False
            elif Manette.Right:
                serv.send(f"{[func, [11], [-0.5]]}".encode('UTF-8'))
                onpeu = False
            continue
