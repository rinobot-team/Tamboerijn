import csv
import json



caminho = "./getupFrontNew.csv"










with open(caminho, newline='',encoding='utf-8') as arquivo:

    leitor = csv.DictReader(arquivo)


    for linha in leitor:
        if linha['HY'] == '':
            print("\n\n\n\n") #pula keyframe versão marcelo
            continue

        MODELO = {
          "duration": None,
          "positions": { 
            "head": {
              "yaw": None,
              "pitch": None
            },
            "left_arm": {
              "shoulder_pitch": None,
              "shoulder_roll": None,
              "elbow_yaw": None,
              "elbow_roll": None,
              "wrist_yaw": None,
              "hand": None
            },
            "right_arm": {
              "shoulder_pitch": None,
              "shoulder_roll": None,
              "elbow_yaw": None,
              "elbow_roll": None,
              "wrist_yaw": None,
              "hand": None
            },
            "left_leg": {
              "hip_yaw_pitch": None,
              "hip_roll": None,
              "hip_pitch": None,
              "knee_pitch": None,
              "ankle_pitch":None,
              "ankle_roll": None
            },
            "right_leg": {
              "hip_yaw_pitch": None,
              "hip_roll": None,
              "hip_pitch": None,
              "knee_pitch": None,
              "ankle_pitch":None,
              "ankle_roll": None
            }
          }
        }

        MODELO['duration'] = float(linha['DUR'])/1000

        #HEAD
        MODELO['positions']['head']['yaw'] = float(linha["HY"])
        MODELO['positions']['head']['pitch'] = float(linha["HP"])

        #LEFT ARM
        MODELO["positions"]['left_arm']['shoulder_pitch'] = float(linha["LSP"])
        MODELO["positions"]['left_arm']['shoulder_roll'] = float(linha["LSR"])
        MODELO["positions"]['left_arm']['elbow_yaw'] = float(linha["LEY"])
        MODELO["positions"]['left_arm']['elbow_roll'] = float(linha["LER"])
        MODELO["positions"]['left_arm']['wrist_yaw'] = float(linha["LWY"])
        MODELO["positions"]['left_arm']['hand'] = float(linha["LH"])


        #RIGHT ARM
        MODELO["positions"]['right_arm']['shoulder_pitch'] = float(linha["RSP"])
        MODELO["positions"]['right_arm']['shoulder_roll'] = float(linha["RSR"])
        MODELO["positions"]['right_arm']['elbow_yaw'] = float(linha["REY"])
        MODELO["positions"]['right_arm']['elbow_roll'] = float(linha["RER"])
        MODELO["positions"]['right_arm']['wrist_yaw'] = float(linha["RWY"])
        MODELO["positions"]['right_arm']['hand'] = float(linha["RH"])
        #LEFT LEG
        MODELO['positions']['left_leg']["hip_yaw_pitch"] = float(linha["LHYP"])
        MODELO['positions']['left_leg']["hip_roll"] = float(linha["LHR"])
        MODELO['positions']['left_leg']["hip_pitch"] = float(linha["LHP"])
        MODELO['positions']['left_leg']["knee_pitch"] = float(linha["LKP"])
        MODELO['positions']['left_leg']["ankle_pitch"] = float(linha["LAP"])
        MODELO['positions']['left_leg']["ankle_roll"] = float(linha["LAR"])

        #RIGHT LEG
        MODELO['positions']['right_leg']["hip_yaw_pitch"] = float(linha["LHYP"]) #DEIXANDO POIS NÃO EXISTE A VERSÃO RIGHT
        MODELO['positions']['right_leg']["hip_roll"] = float(linha["RHR"])
        MODELO['positions']['right_leg']["hip_pitch"] = float(linha["RHP"])
        MODELO['positions']['right_leg']["knee_pitch"] = float(linha["RKP"])
        MODELO['positions']['right_leg']["ankle_pitch"] = float(linha["RAP"])
        MODELO['positions']['right_leg']["ankle_roll"] = float(linha["RAR"])



        print(json.dumps(MODELO, indent=4, ensure_ascii=False)+',')





