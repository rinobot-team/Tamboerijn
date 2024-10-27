# -*- coding: utf-8 -*-

import qi
import sys
import os
import time
import math



class Main():
    def __init__(self, session):
        self.variaveisIntancias()

        while True:
            useSensors  = True
            juntas = [
                
                "HeadPitch",
                "HeadYaw",

                "LHipYawPitch",
                "LHipRoll",
                "LHipPitch",
                "LKneePitch",
                "LAnklePitch",
                "LAnkleRoll",

                "RHipYawPitch",
                "RHipRoll",
                "RHipPitch",
                "RKneePitch",
                "RAnklePitch",
                "RAnkleRoll",

                "LShoulderPitch",
                "LShoulderRoll",
                "LElbowYaw",
                "LElbowRoll",
                "LWristYaw",
                "LHand",

                "RShoulderPitch",
                "RShoulderRoll",
                "RElbowYaw",
                "RElbowRoll",
                "RWristYaw",
                "RHand",
            ]


            sensorAngles = self.motionService.getAngles(juntas, useSensors)

            print("--------------------------------------")
            for junta, angulo in zip(juntas, sensorAngles):
                
                print(u"Ângulo de {}: {}".format(junta, angulo))
            
            print("--------------------------------------")
            os.system('cls')



        


    def variaveisIntancias(self):
        self.motionService = session.service("ALMotion")




if __name__ == "__main__":
    ip = "192.168.0.126"
    porta = 9559

    session = qi.Session()
    

    try:
        session.connect("tcp://" + ip + ":" + str(porta))
    except RuntimeError:
        print (u"Não foi possível conectar no NAO de IP " + ip + " na porta " + str(porta) +".\n")
        sys.exit(1)
    
    os.system('cls')
    print(u"Você se conectou com o NAO.")
    Main(session)
    
    session.close()
    sys.exit(1)

