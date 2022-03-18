import time
import socket
'''
from adafruit_servokit import ServoKit

#==================== Fonction General =======================================================#

kit = Servokit(channels = 16)
Etat = 0
class Servos():

    def __init__(self):

        self.servo1 = kit.servo[11]
        self.servo2 = kit.servo[12]
        self.servo3 = kit.servo[13]
        self.servo4 = kit.servo[14]
        self.servo5 = kit.servo[15]
        self.servo6 = kit.servo[10]
        self.servo7 = kit.servo[9]
        self.servo8 = kit.servo[8]
        self.servo9 = kit.servo[7]
        self.servo10 = kit.servo[6]
        self.servo11 = kit.servo[5]
        self.servo12 = kit.servo[4]

    def angles(self):

        self.servo1.angle = 85
        self.servo2.angle= 85
        self.servo3.angle = 85
        self.servo4.angle = 85
        self.servo5.angle = 85
        self.servo6.angle = 85
        self.servo7.angle = 85
        self.servo8.angle = 85
        self.servo9.angle = 85
        self.servo10.angle = 85
        self.servo11.angle = 85
        self.servo12.angle = 85

servos = Servos()
'''

def Conversion_Chaine_to_List(Chaine):                #Convertisseur de la chaine de carctere recu en liste de valeur >0
    N_chaine = []
    a=''
    for elem in Chaine:
        if elem != ',' :
            a+=elem
        elif elem == ',':
            if a == 'False':
               N_chaine += [False]
            elif a == 'True':
               N_chaine += [True]
            else:
               N_chaine += [float(a)]
            a=''

    if a == 'False':
        N_chaine += [False]
    elif a == 'True':
       N_chaine += [True]
    else:
        N_chaine += [float(a)]
        a=''
    return N_chaine


def StatusMode(ID_Control,Etat):
    ID = Conversion_Chaine_to_List(ID_Control)
    Status = ID[1]
    if ID[0] == 1000:
        if Status == True and Etat == 0:
            Etat = 1
        if Status == True and Etat == 1:
            Etat == 2
        if Status == True and Etat == 2:
            Etat = 3
        if Status == True and Etat == 3:
            Etat = 0
    return Etat



def bras(ID_Control):
    ID = Conversion_Chaine_to_List(ID_Control)

#===================== Bras Droit =======================================================================================#

    if ID[0] == 200:                                  #Id pour le joystic Manette.JR
        X,Y = ID[1],ID[2]                             #les valeurs ID seront convertie en valeur entre 0 et 180

        if X >= 0:
            servos.servos1.angles = X                 #SERVO CENTRALE axe y
            time.sleep(0.1) #A voir si utile
        elif Y >= 0:
            servos.servos3.angles = Y                 #SERVO axe x
            time.sleep(0.1)

    elif ID[0] == 400:                                #Id pour le joystic Manette.RSB  #SERVO ROTATIVE 1
        Status = ID[1]                                #les valeurs ID seront convertie en True ou False qui pourront etre interpreter par le compilateur
        Etat = 0
        if Status == True and Etat == 0:              #ligne pour grader le servo dans une position permanente en appuyant deux fois sur la meme touche
            Etat = 1
        elif Status == True and Etat == 1:
            Etat = 0

        if Etat == 1:
            servos.servos2.angles = 0
            time.sleep(0.1)                           #A voir si utile
        elif Etat == 0:
            servos.servos2.angles = 85
            time.sleep(0.1)

    elif ID[0] == 600:                                #Id pour le joystic Manette.R2   #LE SERVO ROTATIVE 2  reglable
        Pos = ID[1]
        servos.servos4.angles = Pos
        time.sleep(0.1)                               #A voir si utile

    elif ID[0] == 800:                                #Id pour le joystic Manette.R1   # LA PINCE
        Status = ID[1]                                #les valeurs ID seront convertie en True ou False qui pourront etre interpreter par le compilateur

        if Status == True:
            servos.servos5.angles = 0                 # A voir si bon angle
            time.sleep(0.1)                           #A voir si utile
        elif Status == False:
            servos.servos5.angles = 85
            time.sleep(0.1)

#===================== Bras Gauche =======================================================================================#

    if ID[0] == 100:                                  #Id pour le joystic Manette.JL
        X,Y = ID[1],ID[2]                             #les valeurs ID seront convertie en valeur entre 0 et 180

        if X >= 0:                                    #SERVO CENTRALE axe y
            servos.servos6.angles = X
            time.sleep(0.1) #A voir si utile
        elif Y >= 0:
            servos.servos8.angles = Y                 #SERVO axe x
            time.sleep(0.1)

    elif ID[0] == 300:                                #Id pour le joystic Manette.LSB  #SERVO ROTATIVE 1
        Status = ID[1]                                #les valeurs ID seront convertie en True ou False qui pourront etre interpreter par le compilateur
        Etat = 0
        if Status == True and Etat == 0:              #ligne pour grader le servo dans une position permanente en appuyant deux fois sur la meme touche
            Etat = 1
        elif Status == True and Etat == 1:
            Etat = 0

        if Etat == 1:
            servos.servos7.angles = 0
            time.sleep(0.1)                           #A voir si utile
        elif Etat == 0:
            servos.servos7.angles = 85
            time.sleep(0.1)

    elif ID[0] == 500:                                #Id pour le joystic Manette.L2   #LE SERVO ROTATIVE 2  reglable
        Pos = ID[1]
        servos.servos9.angles = Pos
        time.sleep(0.1)                               #A voir si utile

    elif ID[0] == 700:                                #Id pour le joystic Manette.L1   # LA PINCE
        Status = ID[1]                                #les valeurs ID seront convertie en True ou False qui pourront etre interpreter par le compilateur

        if Status == True:
            servos.servos10.angles = 0                # A voir si bon angle
            time.sleep(0.1)                           #A voir si utile
        elif Status == False:
            servos.servos10.angles = 85
            time.sleep(0.1)

def tete(ID_Control):
    ID = Conversion_Chaine_to_List(ID_Control)

    if ID[0] == 100:
        X,Y = ID[1],ID[2]                             #les valeurs ID seront convertie en valeur entre 0 et 180

        if X >= 0:                                    #SERVO CENTRALE axe y
            servos.servos11.angles = X
            time.sleep(0.1) #A voir si utile
        elif Y >= 0:
            servos.servos1.angles = Y                 #SERVO axe x
            time.sleep(0.1)

#==================== Connection Raspberry  et execution ===================================================#
HOST = '' # Server IP or Hostname   # a completer
PORT = 12345 # Pick an open Port (1000+ recommended), must match the client sport
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
print ('Socket created')

#managing error exception
try:
	s.bind((HOST, PORT))
	except socket.error:
	print ('Bind failed ')

	s.listen(5)
	print ('Socket awaiting messages')
	(conn, addr) = s.accept()
	print ('Connected')

# awaiting for message
while True:
	data = conn.recv(1024)
	print ('I sent a message back in response to: ') + data
	reply = ''

    if



	#conn.send(reply)
	conn.close() # Close connections





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
'''
