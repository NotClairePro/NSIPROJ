#from adafruit_servokit import ServoKit
import multiprocessing
import Controls

if __name__ == '__main__':
    Manette = Controls.Ctrl()
    proc = multiprocessing.Process(target=Controls.strt, args = (Manette,))
    proc.start()
    proc.join()
    
    #kit = ServoKit(channels = 14)
    #nbr = int(input('choisire le nbr servo a bouger:'))
    #ang = int(input('choisire le angle:'))
    """
    #while True:
    #    print(Manette2.T)
    #    if Manette2.T is True:
    #        #try:
    #            #kit.servo[nbr].angle = ang
            #except:
            print("amarchpas"+ str(ang) + str(nbr))
        elif Manette2.O is True:
            nbr = int(input('choisire le nbr servo a bouger:'))
        elif Manette2.X is True:
            ang = int(input('choisire le angle:'))
    """

        