
import time
import socket
import board
import neopixel
from adafruit_servokit import ServoKit

# ==================== Fonction General =======================================================#
kit = ServoKit(channels=16)
pixels = neopixel.Neopixel(board.D18, 3)


class Robot:
    def __init__(self):
        """
        :param base:
        """
		self.servos1 = kit.servo[11]
        self.servos2 = kit.servo[12]
        self.servos3 = kit.servo[13]
        self.servos4 = kit.servo[14]
        self.servos5 = kit.servo[15]
        self.servos6 = kit.servo[4]
        self.servos7 = kit.servo[5]
        self.servos8 = kit.servo[6]
        self.servos9 = kit.servo[7]
        self.servos10 = kit.servo[8]
        self.servos11 = kit.servo[10]
        self.servos12 = kit.servo[9]
        self.lServos = [self.servos1, self.servos2, self.servos3, self.servos4, self.servos5, self.servos6, self.servos7,
                       self.servos8, self.servos9, self.servos10, self.servos11, self.servos12]
		self.roues = ["trucs"]
        self.limites = [[1, 170], [1, 170], [1, 170], [1, 170], [1, 170],  # bras gauche
                        [1, 170], [1, 170], [1, 170], [1, 170], [1, 170],  # bras_droit
                        [1, 170], [1, 170]]  # tete

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
		if not verifLimites(listeServo, listeAngle):
			return
        for i in range(len(listeServo)):
            time.sleep(0.1)
            self.lServos[listeServo[i]].angle = listeAngle[i]
	def avance(self, IDS: list, Instructions: list):
		for i in range(len(IDS)):
			self.roues[IDS[i]] = Instructions[i]
		
		

Robot = Robot()
Robot.bougerListeServo([0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11], [85, 85, 85, 85, 85, 85, 85, 85, 85, 85, 85, 85])


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
            conn.send(f"{[motr.angle for motr in Robot.lServos]}".encode('utf-8'))
            continue
        liste = eval(N_data)
        if liste[0] == 'bougerListeServo':
			liste[2] = [85 * (elem+1) for elem in liste[2] ]
            Robot.bougerListeServo(liste[1], liste[2])
