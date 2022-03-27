import time
import socket

from adafruit_servokit import ServoKit

# ==================== Fonction General =======================================================#
kit = ServoKit(channels=16)


class Servos:
    def __init__(self):
        self.servos1 = kit.servo[11]
        self.servos2 = kit.servo[12]
        self.servos3 = kit.servo[13]
        self.servos4 = kit.servo[14]
        self.servos5 = kit.servo[15]
        self.servos6 = kit.servo[10]
        self.servos7 = kit.servo[9]
        self.servos8 = kit.servo[8]
        self.servos9 = kit.servo[7]
        self.servos10 = kit.servo[6]
        self.servos11 = kit.servo[5]
        self.servos12 = kit.servo[4]
        self.lservo = [self.servos1, self.servos2, self.servos3, self.servos4, self.servos5, self.servos6, self.servos7,
                       self.servos8, self.servos9, self.servos10, self.servos11, self.servos12]


class Robot:
    def __init__(self, listeServos: Servo):
        """

        :param listeServos:
        """
        self.bras_droit = listeServos[0:5]
        self.bras_gauche = listeServos[5:10]
        self.tete = listeServos[10:11]
        self.ensemble = {"bras_droit": self.bras_droit, "bras_gauche": self.bras_gauche, "tete": self.tete}

    def __repr__(self):
        return f"""bras_droit = {self.ensemble["bras_droit"]}
        bras_gauche = {self.ensemble["bras_gauche"]}
        tete = {self.ensemble["tete"]}"""

    def setPosition(self, bras_droit=None,
                    bras_gauche=None,
                    tete=None):
        """
        :param bras_droit:
        :param bras_gauche:
        :param tete:
        :return:
        """
        if bras_droit:
            print(bras_droit)
        else:
            print("Pas de bras droit")
            bras_droit = [elem.angle for elem in self.bras_droit]
        if bras_gauche:
            print(bras_gauche)
        else:
            print("Pas de bras gauche")
            bras_gauche = [elem.angle for elem in self.bras_gauche]
        if tete:
            print(tete)
        else:
            print("Pas de tete")
            tete = [elem.angle for elem in self.tete]

        for i in range(len(bras_droit)):
            self.bras_droit[i].angle = bras_droit[i]
        for i in range(len(bras_gauche)):
            self.bras_gauche[i].angle = bras_gauche[i]
        for i in range(len(tete)):
            self.tete[i].angle = tete[i]


servos = Servos()
Robot = Robot(servos.lservo)


def Conversion_Chaine_to_List(Chaine):  # Convertisseur de la chaine de carctere recu, en liste de valeur >0
    N_chaine = []
    a = ''
    for elem in Chaine:
        if elem != ',':
            a += elem
        elif elem == ',':
            if a == 'False':
                N_chaine.append(False)
            elif a == 'True':
                N_chaine.append(True)
            else:
                N_chaine.append(float(a))
            a = ''
    if a == 'False':
        N_chaine.append(False)
    elif a == 'True':
        N_chaine.append(True)
    else:
        N_chaine.append(float(a))
    return N_chaine


# print(Conversion_Chaine_to_List("100,True,False,30,45.5"))

def StatusMode(ID_Control, Etat):
    ID = Conversion_Chaine_to_List(ID_Control)
    Status = ID[1]
    if ID[0] == 1000:
        if Status and Etat == 0:
            Etat = 1
        if Status and Etat == 1:
            Etat = 2
        if Status and Etat == 2:
            Etat = 3
        if Status and Etat == 3:
            Etat = 0
    return Etat


def Limite_Position(ID_control):  # renvoie True ou false
    if servos.servos1.angle == 180:  # revoir
        return servos.servos1.angle == 180
    elif servos.servos1.angle == 60:
        return servos.servos1.angle == 60
    elif servos.servos6.angle == 180:
        return servos.servos6.angle == 180
    elif servos.servos6.angle == 60:
        return servos.servos6.angle == 60
    pass


def bras(ID_Control):
    ID = Conversion_Chaine_to_List(ID_Control)
    # ===================== Bras Droit ===========================================#
    if ID[0] == 200:  # Id pour le joystic Manette.JR
        X, Y = ID[1], ID[2]  # les valeurs ID seront convertie en valeur entre 0 et 180
        if X >= 0:
            servos.servos1.angles = X  # SERVO CENTRALE axe y
            time.sleep(0.1)  # A voir si utile
        elif Y >= 0:
            servos.servos3.angles = Y  # SERVO axe x
            time.sleep(0.1)

    elif ID[0] == 400:  # Id pour le joystic Manette.RSB  #SERVO ROTATIVE 1
        Status = ID[
            1]  # les valeurs ID seront convertie en True ou False qui pourront etre interpreter par le compilateur
        Etat = 0
        if Status and Etat == 0:  # ligne pour grader le servo dans une position permanente en appuyant deux
            # fois sur la meme touche
            Etat = 1
        elif Status and Etat == 1:
            Etat = 0

        if Etat == 1:
            servos.servos2.angles = 0
            time.sleep(0.1)  # A voir si utile
        elif Etat == 0:
            servos.servos2.angles = 85
            time.sleep(0.1)

    elif ID[0] == 600:  # Id pour le joystic Manette.R2   #LE SERVO ROTATIVE 2  reglable
        Pos = ID[1]
        servos.servos4.angles = Pos
        time.sleep(0.1)  # A voir si utile

    elif ID[0] == 800:  # Id pour le joystic Manette.R1   # LA PINCE
        Status = ID[
            1]  # les valeurs ID seront convertie en True ou False qui pourront etre interpreter par le compilateur
        if Status:
            servos.servos5.angles = 0  # A voir si bon angle
            time.sleep(0.1)  # A voir si utile
        elif not Status:
            servos.servos5.angles = 85
            time.sleep(0.1)
    # ===================== Bras Gauche ========================================================#

    if ID[0] == 100:  # Id pour le joystic Manette.JL
        X, Y = ID[1], ID[2]  # les valeurs ID seront convertie en valeur entre 0 et 180
        if X >= 0:  # SERVO CENTRALE axe y
            servos.servos6.angles = X
            time.sleep(0.1)  # A voir si utile
        elif Y >= 0:
            servos.servos8.angles = Y  # SERVO axe x
            time.sleep(0.1)

    elif ID[0] == 300:  # Id pour le joystic Manette.LSB  #SERVO ROTATIVE 1
        Status = ID[
            1]  # les valeurs ID seront convertie en True ou False qui pourront etre interpreter par le compilateur
        Etat = 0
        if Status and Etat == 0:  # ligne pour grader le servo dans une position permanente en appuyant deux
            # fois sur la meme touche
            Etat = 1
        elif Status and Etat == 1:
            Etat = 0

        if Etat == 1:
            servos.servos7.angles = 0
            time.sleep(0.1)  # A voir si utile
        elif Etat == 0:
            servos.servos7.angles = 85
            time.sleep(0.1)

    elif ID[0] == 500:  # Id pour le joystic Manette.L2   #LE SERVO ROTATIVE 2  reglable
        Pos = ID[1]
        servos.servos9.angles = Pos
        time.sleep(0.1)  # A voir si utile

    elif ID[0] == 700:  # Id pour le joystic Manette.L1   # LA PINCE
        Status = ID[
            1]  # les valeurs ID seront convertie en True ou False qui pourront etre interpreter par le compilateur
        if Status:
            servos.servos10.angles = 0  # A voir si bon angle
            time.sleep(0.1)  # A voir si utile
        elif not Status:
            servos.servos10.angles = 85
            time.sleep(0.1)


def tete(ID_Control):
    ID = Conversion_Chaine_to_List(ID_Control)
    if ID[0] == 100:
        X, Y = ID[1], ID[2]  # les valeurs ID seront convertie en valeur entre 0 et 180
        if X >= 0:  # SERVO CENTRALE axe y
            servos.servos11.angles = X
            time.sleep(0.1)  # A voir si utile
        elif Y >= 0:
            servos.servos1.angles = Y  # SERVO axe x
            time.sleep(0.1)


# ==================== Connection Raspberry  et execution ===================================================#
# serveur
# HOST = input(str('Adresse IP du serveur')) # a voir si utile
HOST = ''  # Server IP or Hostname   # a completer #mettre adressse ip du serve et le reporter au clien code poste
PORT = 12345  # Pick an open Port (1000+ recommended), must match the client sport
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
print('Socket created')

# managing error exception
try:
    s.bind((HOST, PORT))
except socket.error:
    print('Bind failed ')

s.listen(5)
print('Socket awaiting messages')
(conn, addr) = s.accept()
print('Connected')
"""
while True:
    data = conn.recv(1024)
    print(data)
    if data == b'terminate':
        conn.close()
        break

    N_data = Conversion_Chaine_to_List(data)
    print(N_data)

    if N_data[0] == 1000:
        StatusMode(N_data, Etat)
        print('Mode:', Etat)

    if Etat == 0:  # mode pour le controle des moteurs avec L2 et R2 pour aller tous ver l avant et L1 et R1 pour
        # marche arriere
        if 500 <= N_data[0] <= 800:
            Moteur(N_data)  # a cree
    elif Etat == 1:  # mode pour le controle des bras
        if 100 <= N_data[0] <= 800:
            Bras(N_data)
    elif Etat == 2:
        if N__data[0] == 100:  # mode pour le controle de la tete
            Tete(N_data)
"""

'''
Les ID_Control

JL = 100
LSB = 300
L1 = 500
L2 = 700

JR = 200
RSB = 400
R1 = 600
R2 = 800

envoie d info sous forme de chaine de carctere avec 2 ou 3 info 
[ ID_control, pos Y,X si joystick ou True ou False si boutton

'''
