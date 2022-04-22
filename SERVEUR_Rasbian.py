import time #biblio pour le temps 
import socket #biblio pour la connection en TCP/IP
import board #biblio pour les pin du raspberry
import neopixel #biblio pour les leds
import RPi.GPIO as GPIO #biblio pour la commandes des sorti GPIO du raspberry
from adafruit_servokit import ServoKit #biblio pour le controle des servos

kit = ServoKit(channels=16) #variable qui definit le nombre de port possible pour le controle des servos -- controle fait par le bias du PCA9586
pixels = neopixel.NeoPixel(board.D18, 3)

#defition des différente sortie liée au controle des différent parti du robot 
GPIO.setmode(GPIO.BCM) #si on met GPIO.BOARD sa  entre en contradiction avec le servokit // le mode BCM c est les indice des GPIO
GPIO.setup(12, GPIO.OUT)  # signal PWM
GPIO.setup(16, GPIO.OUT)
GPIO.setup(25, GPIO.OUT)

GPIO.setup(13, GPIO.OUT)  # signal PWM
GPIO.setup(6, GPIO.OUT)
GPIO.setup(5, GPIO.OUT)
PWM = GPIO.PWM(12, 100)
PWM2 = GPIO.PWM(13, 100)
PWM.start(0) #permet de demarrer le signal qui est initialiser a 0 donc les roues sont a l'arret
PWM2.start(0)

class Robot:
    def __init__(self):
        self.servos1 = kit.servo[11] #definition des différent servo de 1 a 12
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
        self.lServos = [self.servos1, self.servos2, self.servos3, self.servos4, self.servos5, self.servos6, #mise de tous les objet servos dans une liste
                        self.servos7,
                        self.servos8, self.servos9, self.servos10, self.servos11, self.servos12]
        self.roues = [12, 16, 25, 13, 6, 5]# liste des port de connection au raspberry pour le controle des roues
        self.limites = [[0, 150], [0, 180], [0, 180], [0, 180], [65, 130],  # bras gauche      #definition des limites de position de sevos pour eviter leur degradation
                        [30, 180], [0, 180], [0, 180], [0, 180], [40, 95],  # bras_droit
                        [0, 180], [85, 180]]  # tete

    def verifLimites(self, listeServo, listeAngle): #fonction de verification si la liste de valeur verifie bien les condition de limite 
        """
        :param listeServo:
        :param listeAngle:
        :return:
        """
        for i in range(len(listeServo)):
            if not self.limites[listeServo[i]][1] >= listeAngle[i] >= self.limites[listeServo[i]][0]:
                return False
        return True

    def bougerListeServo(self, listeServo, listeAngle): #fonction de mouvement des servos a partir d une liste de donner envoyer
        """
        :param listeServo:
        :param listeAngle:
        :return:
        """
        if not self.verifLimites(listeServo, listeAngle): # verification du respect des limites
            return

        for i in range(len(listeServo)):
            time.sleep(0.1)
            self.lServos[listeServo[i]].angle = listeAngle[i] #on associe a chaque objet servos sa nouvelle position en degré avec des valeurs entre 0 et 180


def avance(IDS: list, Instructions: list): #fonction destiné aux roues
    for i in range(len(IDS)): 
        if IDS[i] == 0 and Instructions[i]<=100: #dans la liste envoyé au verifie quel donné corresponde au PWM ie. au module qui fera varier la vitesse des moteurs
            PWM2.ChangeDutyCycle(Instructions[i])  #la valeur du PWM est entre 0 et 100
        elif IDS[i] == 3:
            if Instructions[i] >=0 and Instructions[i]<=100:
                PWM.ChangeDutyCycle(Instructions[i])
        else:
            GPIO.output(Robot.roues[IDS[i]], bool(Instructions[i])) #pour le reste des informations on les envoie directement au GPIO du cerveau(RASPBERRY)
            #on convertie la liste IDS en liste d'indice des different GPIO a modifier et l' Instruction en valeur de 0 ou 1 avec la fonction bool
        
Robot = Robot()
Robot.bougerListeServo([0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11], [100, 180, 0, 180, 70, 70, 0, 170, 85, 85, 75, 160]) #initialisation des servos a la position de base
pixels[1]= (0,0,255) #on allume une led bleu des le processus fini

HOST = ""  # Ip du serveur   #on effectue la connection avec le poste de commande 
PORT = 34567
CKJ = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
print('wait connection')
try: #test de la connection direct avec la box/reseau internet
# managing error exception
    CKJ.bind((HOST, PORT))
except socket.error:
    print('Bind failed')

CKJ.listen(1)#ecoute du client
print("WAIT")
(conn, addr) = CKJ.accept()#connection du client au serveur
print('Connected by', addr)
pixels[0] = (0, 255, 0)#affichage d une led verte pour la connection effectuer
pixels[2]= (255,0,255)
while True: #on entre dans la boucle infini
    data = conn.recv(1024) #reception des données envoyer par le client 
    if data:
        N_data = data.decode('utf-8') #decodage des donnes selon l encodage UTF-8
        
        if N_data == 'terminate': # si le message est terminate le serveur ferme la connection en arretant les roues et affiche une led rouge
            pixels[0] = (255, 0, 0)
            conn.close()
            PWM.stop()
            PWM2.stop()
            break #arret de la boucle
        
        elif N_data == "getPos": # si le message est getPos alors le serveur envoie les positions en degrés des differents servos 
            conn.send(f"{[motr.angle for motr in Robot.lServos]}".encode('utf-8')) #envoie une liste par comprehension
            continue
            
        liste = eval(N_data) #convertie les données de string a list
        print(liste)
              
        if abs(liste[2][0]) == 5:
            liste[2][0] = Robot.lServos[liste[1][0]].angle + (10 + (20 * -(liste[2][0] == -5)))
        if max(liste[2]) < 1.3:
            l = []
            for i in range(len(liste[2])):
                liste[2][i] = Robot.limites[liste[1][i]][0] + ( (Robot.limites[liste[1][i]][1]- Robot.limites[liste[1][i]][0]) /2) * (liste[2][i]+1)
            
        if liste[0] == 'bougerListeServo':#cette conparaison permet de veriffeir dans quel mode de mouvement entrer
            if liste[2] == [100, 180, 0, 180, 70, 70, 0, 170, 85, 85, 75, 160]: #si la liste de donnet correspond au default alors on allume la led bleu
                pixels[1]= (0,0,255)
                Robot.bougerListeServo(liste[1], liste[2])
    
            Robot.bougerListeServo(liste[1], liste[2]) # sinon la couleur change en cyan
            pixels[1]= (0,255,255)
            
        if liste[0] == 'avancer': #cette conparaison permet de veriffeir dans quel mode de mouvement entrer
            if liste[2]==[0,False,False,0,False,False]: #si la liste de données correnspons a la valuer nul sur toutes es position alors les rous s arrete 
                avance(liste[1], [0,0,0,0,0,0])
                pixels[2]= (255,0,255)
                GPIO.output(12,False) #desactivation du PWM
                GPIO.output(13,False)
                
            GPIO.output(12,True)#sinon on reactive le PWM et on lit la liste de donnée 
            GPIO.output(13,True)
            avance(liste[1], liste[2])
            pixels[2]= (255,255,0)
            
        conn.send('done'.encode('utf-8'))#a la fin de chaque action le serveur envie done pour dire qu il peut realiser une nouvelle demande, 
        #ce dispositive permet de limité les beugs et la surcharge du cerveau au niveau de la lecture de donnée
        
 '''
 le signa PWM est un signal modulaire qui sur une certaine periode temps envoie un signal electrique au module de vitesse des 2 moteurs de 12V
 et en fonction de la fréquence d envoie du signal entre 0 et 100 le module le convertie en courrant de 12V qui est modulée entre 0 et 12V avec une intensité 
 de 600mA sur chaque moteur, si par exemple en envoie un signal PWM de 75 le courrant déservit sera de ~ 9V
 '''
 

