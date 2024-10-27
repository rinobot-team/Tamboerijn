# -*- coding: utf-8 -*-

import qi
import sys
import os

import json
import codecs
import time


class Main():
    def __init__(self, session):
        self.variaveisIntancias()

        with codecs.open('coreografia.json', 'r', 'utf-8') as arquivo_json:
            self.coreografia = json.load(arquivo_json)

        self.energizar()

        #o que ce quer fazer

        self.desenergizar()
        
        





    def initial(self):
        nomesJuntas = self.coreografia["initial"]["keyframe"].keys()
        valoresAngulos = self.coreografia["initial"]["keyframe"].values()
        duration = self.coreografia["initial"]['duration']

        self.motionService.setStiffnesses(nomesJuntas, 1.0)
        self.motionService.setAngles(nomesJuntas, valoresAngulos, duration)


    def currentCoreo(self):
        frames = len(self.coreografia['keyframes'])
        for frame in range(0,frames):
            nomesJuntas = self.coreografia["keyframes"][frame]["keyframe"].keys()
            valoresAngulos = self.coreografia["keyframes"][frame]["keyframe"].values()
            duration = self.coreografia["keyframes"][frame]['duration']

            self.motionService.setStiffnesses(nomesJuntas, 1.0)
            self.motionService.setAngles(nomesJuntas, valoresAngulos, duration)
            print("KEYFRAME: ", frame)
            time.sleep(3)

    def variaveisIntancias(self):
        self.motionService = session.service("ALMotion")
        self.voiceService = session.service("ALTextToSpeech")
        self.posture = session.service("ALRobotPosture")
        

    def crouch(self):
        self.posture.goToPosture("Crouch", 1.0)

    def energizar(self):
        self.motionService = session.service("ALMotion")
        self.motionService.wakeUp()


    def desenergizar(self):
        self.motionService = session.service("ALMotion")

        self.motionService.rest()

    def falar(self, texto, volume):
        self.voiceService.setLanguage("English")
        self.voiceService.setVolume(volume)
        self.voiceService.say(texto)





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

