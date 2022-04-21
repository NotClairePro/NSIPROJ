import socket #biblio pour la connection TCP/IP
import time #biblio pour le temps
from Ctrls import Strt, Controls

#Connection au serveur ==> ROBOT
HOST = "192.168.1.61"  # The server's hostname or IP address
PORT = 34567  # The port used by the server
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
    while True: # on entre dans la boucle infini
        Strt(Manette) 
        if onpeu is False:
            dat = serv.recv(1024)
            if dat:
                if dat.decode('utf-8') == "done":
                    onpeu = True
            continue

        if Manette.L1 and Manette.R1 and Manette.L2 and Manette.R2: #si toutes ces bouttons son maintenu alors la connection est terminer et la boucle s arrete
            serv.send("terminate".encode("UTF-8"))
            break

        elif Manette.L1: # si on maintient L1 alors on est dans le mode de Choix du servChoisi a bouger:
            if Manette.T: #chaque boutton correspond a un servo 
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
        elif Manette.R1: #si R1 est maintenus on peut mannipuler le servo choisis avant avec avec les boutton UP/RIGHT/LEFT/DOWN 
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
        elif Manette.T: #si on maintient le bouton triangle alors on peut avancer avec le robot
            if Manette.R2 and Manette.L2: #les deux roux fonctionne
                serv.send(
                    f"{['avancer', [0, 1, 2, 3, 4, 5], [int(Manette.L2 * 50),True, False, int(Manette.R2 * 50), True, False]]}".encode(
                        'UTF-8'))
                onpeu = False
                continue
            elif Manette.R2: #la roue droite est en marche
                serv.send(
                    f"{['avancer', [0, 1, 2], [int(Manette.R2 * 50), True , False]]}".encode(
                        'UTF-8'))
                onpeu = False
                continue
            elif Manette.L2: #la roue gauche est en marche
                serv.send(
                    f"{['avancer', [3, 4, 5], [int(Manette.L2 * 50), True,False]]}".encode(
                        'UTF-8'))
                onpeu = False
                continue
            else : #si R2 ou L2 ne sont pas appuyer allors on envoie la liste de valeurs nul ou false
                serv.send(
                    f"{['avancer', [0, 1, 2, 3, 4, 5], [0, False,False,0, False, False]]}".encode(
                        'UTF-8'))
                time.sleep(0.1)
                onpeu = False
                continue

        elif Manette.X: #meme chose qu plus haut mais ici on est dans le mode pour reculer
            if Manette.R2 and Manette.L2:
                serv.send(
                    f"{['avancer', [0, 1, 2, 3, 4, 5], [int(Manette.L2 * 50), False, True, int(Manette.R2 * 50), False, True]]}".encode(
                        'UTF-8'))
                onpeu = False
                continue
            elif Manette.R2:
                serv.send(
                    f"{['avancer', [0, 1, 2], [int(Manette.R2 * 50), False, True]]}".encode(
                        'UTF-8'))
                onpeu = False
                continue
            elif Manette.L2:
                serv.send(
                    f"{['avancer', [3, 4, 5], [int(Manette.L2 * 50), False, True]]}".encode(
                        'UTF-8'))
                onpeu = False
                continue
            else:
                serv.send(
                    f"{['avancer', [0, 1, 2, 3, 4, 5], [0, False, False, 0, False, False]]}".encode(
                        'UTF-8'))
                time.sleep(0.1)
                onpeu = False
                continue
                
        elif Manette.RSB: #si maintenu alors on est dans le mode d'enregistrement des position, du choix de la position, mise en position ou supression d une position
            
            if Manette.Menu: #mode de mise en position 
                serv.send(f"{[func, [o for o in range(12)], dictPositions[Names[CurrentPos]]]}".encode('UTF-8')) #envoie des position de servo coorespondant au nom de la positon dans le doc position.txt
                onpeu = False

            elif Manette.Up: #mode de choix de la postion 
                CurrentPos = CurrentPos + (CurrentPos + 1 < len(Names))
                time.sleep(0.2)
                print(f'Position choisi:{Names[CurrentPos]}') #en fonction du nombre d appuie sur le bouton en defini l'indice de la position qui sera ensuite chercher dans le doc

            elif Manette.Down: #mode de choix de la postion
                CurrentPos = CurrentPos - (CurrentPos > 0)
                time.sleep(0.2)
                print(f'Position choisi:{Names[CurrentPos]}') #en fonction du nombre d appuie sur le bouton en defini l'indice de la position qui sera ensuite chercher 

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
            elif Manette.JR != [0, 0]:  # servChoisi 0 et servChoisi 2 = bras droit
                angles = Manette.JR
                for k in range(len(angles)):
                    if angles[k] > 1:
                        angles[k] = 1
                    elif angles[k] < -1:
                        angles[k] = -1

                serv.send(f"{[func, [7, 5], angles]}".encode('UTF-8'))
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
