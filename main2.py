# from adafruit_servokit import ServoKit

from Ctrls import Strt, Controls

if __name__ == '__main__':
    Manette = Controls()
    while True:
        Strt(Manette)
        Id_control = 0
        if Manette.JL != [0, 0]:
            Id_control = "100"
        elif Manette.LSB:
            Id_control = "300"
        elif Manette.L1:
            Id_control = "500"
        elif Manette.L2:
            Id_control = "700"
        elif Manette.JR != [0, 0]:
            Id_control = "200"
        elif Manette.RSB:
            Id_control = "400"
        elif Manette.R1:
            Id_control = "600"
        elif Manette.R2:
            Id_control = "800"
        elif Manette.Opt:
            Etat = 1
        elif Manette.Share:
            Etat = 2
        elif Manette.Menu:
            Etat = 0
        # elif Manette.A:

        print(Id_control)
