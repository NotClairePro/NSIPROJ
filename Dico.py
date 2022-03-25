class Servo:
    def __init__(self):
        self.servo1 = "truc1"
        self.servo2 = "truc2"
        self.servo3 = "truc3"
        self.servo4 = "truc4"
        self.servo5 = "truc5"
        self.servo6 = "truc6"
        self.servo7 = "truc7"
        self.servo8 = "truc8"
        self.servo9 = "truc9"
        self.servo10 = "truc10"
class Robot:
    def __init__(self, servo_droit: list, servo_gauche: list[object], servo_tete: object):
        """
        :param servo_droit: list of servo objects
        :param servo_gauche: list of servo objects
        :param servo_tete: servo object
        """
        self.bras_droit = servo_droit
        self.bras_gauche = servo_gauche
        self.tete = servo_tete

A= Robot([servo1,servo2],[],[])