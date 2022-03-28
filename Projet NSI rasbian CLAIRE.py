import time
import socket
import board 
import neopixel
from adafruit_servokit import ServoKit

# ==================== Fonction General =======================================================#
kit = ServoKit(channels=16)
pixels = neopixel.Neopixel(board.D18,3)

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
    def __init__(self, base: Servos):
        """
        :param base:
        """
        self.base = base
        listeServos = base.lservo
        self.bras_droit = listeServos[0:5]
        self.bras_gauche = listeServos[5:10]
        self.tete = listeServos[10:12]
        self.ensemble = {"bras_droit": self.bras_droit, "bras_gauche": self.bras_gauche, "tete": self.tete}

    def __repr__(self):
        return f"""bras_droit = {self.ensemble["bras_droit"]}
        bras_gauche = {self.ensemble["bras_gauche"]}
        tete = {self.ensemble["tete"]}"""

    def setPosition(self, bras_droit: list[tuple[int]] = None,
                    bras_gauche: list[tuple[int]] = None,
                    tete: list[tuple[int]] = None):
        """
        :param bras_droit:
        :param bras_gauche:
        :param tete:
        :return:
        """
        if bras_droit:
            for i in range(len(bras_droit[0])):
                self.bras_droit[0][i].angle = bras_droit[1][i]
        if bras_gauche:
            for i in range(len(bras_gauche[0])):
                self.bras_gauche[0][i].angle = bras_gauche[1][i]
        if tete:
            for i in range(len(tete[0])):
                self.tete[0][i].angle = tete[1][i]

    def bougerListeServo(self, listeServo, listeAngle):
        """
        :param listeServo:
        :param listeAngle:
        :return:
        """
        for i in range(len(listeServo)):
            self.base.lservo[listeServo[i]].angle = listeAngle[i]


servos = Servos()
Robot = Robot(servos)
Robot.bougerListeServo([0,1,2,3,4,5,6,7,8,9,10,11], [85,85,85,85,85,85,85,85,85,85,85,85])
# l'idée est de recevoir une série d'informations pour le serveur:
# 1. la fonction à appeler (en fonction de quel bouton est préssé côté client)
# 2. les arguments de la fonction

# par exemple : ["setPosition", [(1,85),(2,85),(3,85)], [(1,85),(2,85),(3,85)] ]
# cela veut dire que l'on veut appeler la fonction setPosition avec les arguments suivants :
# 1. bras_droit = [(1,85),(2,85),(3,85),(4,85),(5,85)]
# 2. bras_gauche = [(1,85),(2,85),(3,85),(4,85),(5,85)]


HOST = "" #Ip du serveur 
PORT = 12345
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
print('Socket created')

# managing error exception
try:
    s.bind((HOST, PORT))
except socket.error:
    print('Bind failed ')
    sys.exit()

s.listen(5)
print('Socket awaiting messages')
(conn, addr) = s.accept()
print('Connected')
if (conn, addr) = s.accept():
    pixels[0] = (0,255,0)

while True:
    data = conn.recv(1024)
    print(data)
    if data == 'terminate':
        conn.close()
        break
    N_data = list(data.decode('utf-8'))
    print(N_data)
    Robot.setPosition(N_data)
    
                       
   
    

