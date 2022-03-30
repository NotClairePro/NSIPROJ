
import time
import socket
import board
import neopixel
from adafruit_servokit import ServoKit

# ==================== Fonction General =======================================================#
kit = ServoKit(channels=16)
pixels = neopixel.Neopixel(board.D18, 3)

sens = int(input("sensi: "))
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
        self.bras_gauche = listeServos[0:5]
        self.bras_droit = listeServos[5:10]
        self.tete = listeServos[10:12]
        self.limites = [[1, 120], [1, 120], [1, 120], [1, 120], [1, 120],  # bras gauche
                        [1, 120], [1, 120], [1, 120], [1, 120], [1, 120],  # bras_droit
                        [1, 120], [1, 120]]  # tete

    def __repr__(self):
        return f"""bras_gauche = {self.bras_gauche}
        bras_droit = {self.bras_droit}
        tete = {self.tete}"""

    def verifLimites(self, listeServo, listeAngle):
        """
        :param listeServo:
        :param listeAngle:
        :return:
        """
        for i in range(len(listeServo)):
            if not self.limites[listeServo[i]][1] > listeAngle[i] < self.limites[listeServo[i]][0]:
                return False
        return True

    def bougerListeServo(self, listeServo, listeAngle):
        """
        :param listeServo:
        :param listeAngle:
        :return:
        """
        for i in range(len(listeServo)):
            time.sleep(0.5)
            self.base.lservo[listeServo[i]].angle = listeAngle[i]


servos = Servos()
Robot = Robot(servos)
Robot.bougerListeServo([0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11], [85, 85, 85, 85, 85, 85, 85, 85, 85, 85, 85, 85])
# l'idée est de recevoir une série d'informations pour le serveur:
# 1. la fonction à appeler (en fonction de quel bouton est préssé côté client)
# 2. les arguments de la fonction

# par exemple : ["setPosition", [(1,85),(2,85),(3,85)], [(1,85),(2,85),(3,85)] ]
# cela veut dire que l'on veut appeler la fonction setPosition avec les arguments suivants :
# 1. bras_droit = [(1,85),(2,85),(3,85),(4,85),(5,85)]
# 2. bras_gauche = [(1,85),(2,85),(3,85),(4,85),(5,85)]


HOST = ""  # Ip du serveur
PORT = 45554
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# managing error exception
s.bind((HOST, PORT))
s.listen(1)

conn, addr = s.accept()
print('Connected by', addr)
pixels[0] = (0, 255, 0)

while True:
    data = conn.recv(1024)
    if data:
        N_data = data.decode('utf-8')

        if N_data == 'terminate':
            conn.close()
            break
        if N_data == "getPos":
            conn.send(f"{[mot.angle for mot in servos.lservo]}".encode('utf-8'))
            continue
        liste = eval(N_data)

        liste[2] = [servos.lservo[liste[1][i]].angle - round(liste[2][i] * sens) for i in liste[2]]
        if liste[0] == 'bougerListeServo':
            Robot.bougerListeServo(liste[1], liste[2])
