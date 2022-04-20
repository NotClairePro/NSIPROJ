import time
import socket
import sys
import board
import neopixel
import RPi.GPIO as GPIO
from adafruit_servokit import ServoKit
kit = ServoKit(channels=16)
pixels = neopixel.NeoPixel(board.D18, 3)

GPIO.setmode(GPIO.BCM) #si on met GPIO.BOARD sa  entre en contradiction avec le servokit // le mode BCM c est les indice des GPIO
GPIO.setup(12, GPIO.OUT)  # signal PWM
GPIO.setup(16, GPIO.OUT)
GPIO.setup(25, GPIO.OUT)

GPIO.setup(13, GPIO.OUT)  # signal PWM
GPIO.setup(6, GPIO.OUT)
GPIO.setup(5, GPIO.OUT)
PWM = GPIO.PWM(12, 100)
PWM2 = GPIO.PWM(13, 100)
PWM.start(0)
PWM2.start(0)

class Robot:
    def __init__(self):
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
        self.lServos = [self.servos1, self.servos2, self.servos3, self.servos4, self.servos5, self.servos6,
                        self.servos7,
                        self.servos8, self.servos9, self.servos10, self.servos11, self.servos12]
        self.roues = [12, 16, 25, 13, 6, 5]
        self.limites = [[0, 150], [0, 180], [0, 180], [0, 180], [65, 130],  # bras gauche
                        [30, 180], [0, 180], [0, 180], [0, 180], [40, 95],  # bras_droit
                        [0, 180], [85, 180]]  # tete

    def verifLimites(self, listeServo, listeAngle):
        """
        :param listeServo:
        :param listeAngle:
        :return:
        """
        for i in range(len(listeServo)):
            if not self.limites[listeServo[i]][1] >= listeAngle[i] >= self.limites[listeServo[i]][0]:
                return False
        return True

    def bougerListeServo(self, listeServo, listeAngle):
        """
        :param listeServo:
        :param listeAngle:
        :return:
        """
        if not self.verifLimites(listeServo, listeAngle):
            return

        for i in range(len(listeServo)):
            time.sleep(0.1)
            self.lServos[listeServo[i]].angle = listeAngle[i]


def avance(IDS: list, Instructions: list):
    for i in range(len(IDS)):
        if IDS[i] == 0 and Instructions[i]<=100:
            PWM2.ChangeDutyCycle(Instructions[i])  
        elif IDS[i] == 3:
            if Instructions[i] >=0 and Instructions[i]<=100:
                PWM.ChangeDutyCycle(Instructions[i])
        else:
            GPIO.output(Robot.roues[IDS[i]], bool(Instructions[i]))
        
Robot = Robot()
Robot.bougerListeServo([0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11], [100, 180, 0, 180, 70, 70, 0, 170, 85, 85, 75, 160])
pixels[1]= (0,0,255)

HOST = ""  # Ip du serveur
PORT = 34567
CKJ = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
print('wait connection')
try:
# managing error exception
    CKJ.bind((HOST, PORT))
except socket.error:
    print('Bind failed')

CKJ.listen(1)
print("truc")
(conn, addr) = CKJ.accept()
print('Connected by', addr)
pixels[0] = (0, 255, 0)
pixels[2]= (255,0,255)
while True:
    data = conn.recv(1024)
    if data:
        N_data = data.decode('utf-8')
        
        if N_data == 'terminate':
            pixels[0] = (255, 0, 0)
            conn.close()
            PWM.stop()
            PWM2.stop()
            break
        
        elif N_data == "getPos":
            conn.send(f"{[motr.angle for motr in Robot.lServos]}".encode('utf-8'))
            continue
        liste = eval(N_data)
        print(liste)
        
        if liste[0] == 'calmetoi':
            avance(liste[1], liste[2])
            conn.send('cbon'.encode('utf-8'))
            continue
        
        if abs(liste[2][0]) == 5:
            liste[2][0] = Robot.lServos[liste[1][0]].angle + (10 + (20 * -(liste[2][0] == -5)))
        if max(liste[2]) < 1.3:
            liste[2] = [85 * (elem+1) for elem in liste[2] ]
            
        if liste[0] == 'bougerListeServo':
            if liste[2] == [100, 180, 0, 180, 70, 70, 0, 170, 85, 85, 75, 160]:
                pixels[1]= (0,0,255)
                Robot.bougerListeServo(liste[1], liste[2])
                
            pixels[1]= (0,255,255)
            Robot.bougerListeServo(liste[1], liste[2])
        
        if liste[0] == 'avancer':
            if liste[2]==[0,False,False,0,False,False]:
                avance(liste[1], [0,0,0,0,0,0])
                pixels[2]= (255,0,255)
                GPIO.output(12,False)
                GPIO.output(13,False)
                print('pass3')
            GPIO.output(12,True)
            GPIO.output(13,True)
            avance(liste[1], liste[2])
            pixels[2]= (255,255,0)
        conn.send('done'.encode('utf-8'))
        

