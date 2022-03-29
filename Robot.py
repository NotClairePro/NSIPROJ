# On va envoyer une série de commandes au wall-E
# on va donc définir un ensemble de methodes qui seront appelées sur la classe Robot
# Les methodes seront les suivantes:
# - bougerServo(self, degrés, vitesse, id de Servo)

class truc:
    def __init__(self, nom):
        self.nom = nom
        self.angle = 85

    def __repr__(self):
        return f"{self.nom}: {self.angle}"


class Servo:
    def __init__(self):
        self.servo1 = truc("truc1")
        self.servo2 = truc("truc2")
        self.servo3 = truc("truc3")
        self.servo4 = truc("truc4")
        self.servo5 = truc("truc5")
        self.servo6 = truc("truc6")
        self.servo7 = truc("truc7")
        self.servo8 = truc("truc8")
        self.servo9 = truc("truc9")
        self.servo10 = truc("truc10")
        self.servo11 = truc("truc11")
        self.servo12 = truc("truc12")
        self.lservo = [self.servo1, self.servo2, self.servo3, self.servo4, self.servo5, self.servo6,
                       self.servo7, self.servo8, self.servo9, self.servo10, self.servo11, self.servo12]

        for elem in self.lservo:
            elem.angle = 85


class Robot:
    def __init__(self, listeServos: Servo):
        """

        :param listeServos:
        """
        self.bras_droit = listeServos[0:5]
        self.bras_gauche = listeServos[5:10]
        self.tete = listeServos[10:12]
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


servos = Servo()
Robot = Robot(servos.lservo)
print(Robot)
Robot.setPosition()
print(Robot)
Robot.setPosition(bras_droit=[90, 90, 90, 90, 90], bras_gauche=[90, 90, 90, 90, 90], tete=[90,90])

print(Robot)
