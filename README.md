# Projet Final NSI

Projet Nsi Jules, Claire et Kamil <br/>
Le projet est un robot, stylisé sur le dessin animé Wall-E. <br/>
Pour le contrôle on utilise un Raspberry Pi ZERO W qui sert de serveur. <br/>
Ce serveur est connecté a un poste de commande, <br/> ici un ordinateur portable étant connecté sur un même réseau que le Raspberry. <br/>
Pour le contôle on utilise le protocole TCP/IP qui envoie les information par wifi. <br/>
Pour la manipulation des servos, on utilise un module de démultiplication du signal PWM, le PCA9586. <br/>
Le contrôle de se module se fait à partir le la bibliothèque Adafruit SERVOKIT qui permet le contôle de 16 servomoteurs sur un module. <br/>
Pour le contrôle des roues on utilise le module L293D contrôler par les GPIO du Raspberry. <br/>
