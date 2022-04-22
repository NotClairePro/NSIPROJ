import pygame

pygame.init()
joysticks = []
clock = pygame.time.Clock()
keepPlaying = True
# for al the connected joysticks
for i in range(0, pygame.joystick.get_count()):
    # create an Joystick object in our list
    joysticks.append(pygame.joystick.Joystick(i))
    # initialize them all (-1 means loop forever)
    joysticks[-1].init()
    # print a statement telling what the name of the controller is
    print("Detected joystick "), joysticks[-1].get_name(), "'"


class Controls:
    def __init__(self):
        self.X = False
        self.R = False
        self.T = False
        self.C = False
        self.L1 = False
        self.R1 = False
        self.L2 = 0
        self.R2 = 0
        self.Share = False
        self.Opt = False
        self.Menu = False
        self.LSB = False
        self.RSB = False
        self.Up = False
        self.Down = False
        self.Left = False
        self.Right = False
        self.JL = [0, 0]
        self.JR = [0, 0]
        self.TouchPad = [0, 0]

    def __repr__(self):
        r = f"X:{self.X}, Rond:{self.R}, Triangle:{self.T}, Carré:{self.C} \n" f"L1:{self.L1}, R1:{self.R1}, " \
            f"L2:{self.L2}, R2:{self.R2} \n" f"Share:{self.Share}, Opt:{self.Opt}, Menu:{self.Menu}" \
            f", Pad:{self.Up};{self.Down};{self.Right};{self.Left} \n" f"LSB:{self.LSB}, RSB:{self.RSB}" \
            f" \n" f"JL:{self.JL}, JR:{self.JR} \n "
        print(r)
        return r

    def reset(self): #après une commande, les valeurs des commandes doivent être mis à False, afin d'éviter qu'un servo-moteur soit constamment appelé jusqu'à ce qu'il arrête de fonctionner 
        self.X = False
        self.R = False
        self.T = False
        self.C = False
        self.L1 = False
        self.R1 = False
        self.Share = False
        self.Opt = False
        self.Menu = False
        self.LSB = False
        self.RSB = False
        self.Up = False
        self.Down = False
        self.Left = False
        self.Right = False


def Strt(Manette):
    while keepPlaying:
        clock.tick(60)
        for event in pygame.event.get():

            if event.type == pygame.JOYAXISMOTION: #if Joysticks are moved in X or Y axis
                if event.axis < 2:
                    if 0.1 > event.value > -0.1:
                        Manette.JL[event.axis] = 0
                    else:
                        Manette.JL[event.axis] = event.value

                elif event.axis < 4:
                    if 0.1 > event.value > -0.1:
                        Manette.JR[event.axis - 2] = 0
                    else:
                        Manette.JR[event.axis - 2] = event.value
                elif event.axis == 4:
                    if event.value + 1 < 0.0003:
                        Manette.L2 = 0
                    else:
                        Manette.L2 = event.value + 1
                elif event.axis == 5:
                    if event.value + 1 < 0.0003:
                        Manette.R2 = 0
                    else:
                        Manette.R2 = event.value + 1
            elif event.type == pygame.JOYBUTTONDOWN: # checks if any button (X,Y,A,B) is pressed down
                if event.button == 0:
                    Manette.X = True
                elif event.button == 1:
                    Manette.R = True
                elif event.button == 2:
                    Manette.C = True
                elif event.button == 3:
                    Manette.T = True
                elif event.button == 4:
                    Manette.Share = True
                elif event.button == 5:
                    Manette.Menu = True
                elif event.button == 6:
                    Manette.Opt = True
                elif event.button == 7:
                    Manette.LSB = True
                elif event.button == 8:
                    Manette.RSB = True
                elif event.button == 9:
                    Manette.L1 = True
                elif event.button == 10:
                    Manette.R1 = True
                elif event.button == 11:
                    Manette.Up = True
                elif event.button == 12:
                    Manette.Down = True
                elif event.button == 13:
                    Manette.Left = True
                elif event.button == 14:
                    Manette.Right = True
            elif event.type == pygame.JOYBUTTONUP: #checks if the user stopped pressing any specific button
                if event.button == 0:
                    Manette.X = False
                elif event.button == 1:
                    Manette.R = False
                elif event.button == 2:
                    Manette.C = False
                elif event.button == 3:
                    Manette.T = False
                elif event.button == 4:
                    Manette.Share = False
                elif event.button == 5:
                    Manette.Menu = False
                elif event.button == 6:
                    Manette.Opt = False
                elif event.button == 7:
                    Manette.LSB = False
                elif event.button == 8:
                    Manette.RSB = False
                elif event.button == 9:
                    Manette.L1 = False
                elif event.button == 10:
                    Manette.R1 = False
                elif event.button == 11:
                    Manette.Up = False
                elif event.button == 12:
                    Manette.Down = False
                elif event.button == 13:
                    Manette.Left = False
                elif event.button == 14:
                    Manette.Right = False
            elif event.type == pygame.CONTROLLERTOUCHPADMOTION: #checks for use of touch pad
                Manette.TouchPad = [event.x, event.y]
        break