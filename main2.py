# from adafruit_servokit import ServoKit

from Ctrls import Strt, Controls

if __name__ == '__main__':
    Manette = Controls()
    while True:
        Strt(Manette)
        if Manette.B:
            print("boop?")
        elif Manette.A:
            print("boop?")
        elif Manette.A:
            print("boop?")
