import pygame


class Ctrl:
    def __init__(self):
        self.init = False
        self.C = False
        self.X = False
        self.T = False
        self.O = False
        self.L1 = False
        self.R1 = False
        self.L2 = 0
        self.R2 = 0
        self.Share = False
        self.Opt = False
        self.Menu = False
        self.LSB = False
        self.RSB = False
        self.Pad = False
        self.JL = [0, 0]
        self.JR = [0, 0]

    def __repr__(self):
        r = f"Carre:{self.C}, X:{self.X}, Triangle:{self.T}, O:{self.O} \n" f"L1:{self.L1}, R1:{self.R1}, L2:{self.L2}, R2:{self.R2} \n" f"Share:{self.Share}, Opt:{self.Opt}, Menu:{self.Menu}, Pad:{self.Pad} \n" f"LSB:{self.LSB}, RSB:{self.RSB} \n" f"JL:{self.JL}, JR:{self.JR} \n"
        print(r)
        return r


def strt(Manette):
    pygame.init()
    joysticks = []
    clock = pygame.time.Clock()
    # for al the connected joysticks
    for i in range(0, pygame.joystick.get_count()):
        # create an Joystick object in our list
        joysticks.append(pygame.joystick.Joystick(i))
        # initialize them all (-1 means loop forever)
        joysticks[-1].init()
        # print a statement telling what the name of the controller is
        print("Detected joystick "), joysticks[-1].get_name(), "'"

    while True:
        Manette.init = True
        clock.tick(10)
        for event in pygame.event.get():
            # The 0 button is the 'a' button, 1 is the 'b' button, 2 is the 'x' button, 3 is the 'y' button
            if event.type == pygame.JOYAXISMOTION:
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
                        Manette.R2 = 0
                    else:
                        Manette.R2 = event.value + 1
                elif event.axis == 5:
                    if event.value + 1 < 0.0003:
                        Manette.L2 = 0
                    else:
                        Manette.L2 = event.value + 1
            elif event.type == pygame.JOYBUTTONDOWN:
                if event.button == 0:
                    Manette.C = True
                elif event.button == 1:
                    Manette.X = True
                elif event.button == 2:
                    Manette.O = True
                elif event.button == 3:
                    Manette.T = True
                elif event.button == 4:
                    Manette.L1 = True
                elif event.button == 5:
                    Manette.R1 = True
                elif event.button == 8:
                    Manette.Share = True
                elif event.button == 9:
                    Manette.Opt = True
                elif event.button == 10:
                    Manette.LSB = True
                elif event.button == 11:
                    Manette.RSB = True
                elif event.button == 12:
                    Manette.Menu = True
                elif event.button == 13:
                    Manette.Pad = True

            elif event.type == pygame.JOYBUTTONUP:
                if event.button == 0:
                    Manette.C = False
                elif event.button == 1:
                    Manette.X = False
                elif event.button == 2:
                    Manette.O = False
                elif event.button == 3:
                    Manette.T = False
                elif event.button == 4:
                    Manette.L1 = False
                elif event.button == 5:
                    Manette.R1 = False
                elif event.button == 8:
                    Manette.Share = False
                elif event.button == 9:
                    Manette.Opt = False
                elif event.button == 10:
                    Manette.LSB = False
                elif event.button == 11:
                    Manette.RSB = False
                elif event.button == 12:
                    Manette.Menu = False
                elif event.button == 13:
                    Manette.Pad = False
