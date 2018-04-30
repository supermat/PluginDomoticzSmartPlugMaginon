# import socket
# import argparse
# import json
# import time
# import datetime
# import sys
import telnetlib,json

class Smartplug:
    def __init__(self, p_ip):
        self._ip = p_ip
    
    def read(self):
        v_retour = "Success"
        user = b"admin"
        password = b"admin"
        try:
            tn = telnetlib.Telnet(self._ip,timeout=1)
            tn.read_until(b"login: ")
            tn.write(user + b"\n")
            if password:
                tn.read_until(b"Password: ")
                tn.write(password + b"\n")
            tn.read_until(b"commands.", 2)
            tn.write(b"GetInfo W\n")
            tn.write(b"GetInfo V\n")
            tn.write(b"GetInfo I\n")
            tn.write(b"GetInfo E\n")
            tn.write(b"exit\n")
            self._response = tn.read_all()
            tn.close()

            for line in str(self._response).split('\\r\\n'):
                if line.startswith("$01W"):
                    self._power =  float(line[7:11]+ '.' + line[11:])
                    if self._power > 0.2:
                        self._etat = 1
                    else: self._etat = 0
                elif line.startswith("$01V"):
                    self._voltage = float(line[7:10] + '.' + line[10:])
                elif line.startswith("$01I"):
                    self._intensite =   float(line[7:9]+ '.' + line[9:])
                elif line.startswith("$01E"):
                    self._compteur =  float(line[7:11]+ '.' + line[11:])
        
        except:
            v_retour = 'Failed'
        finally:
            return v_retour
    
    def getInfo(self):
        v_strjson = '{'
        v_strjson += '"etat":"'+str(self._etat)+'"'
        v_strjson += ',"puissance":"'+str(self._power)+'"'
        v_strjson += ',"tension":"'+str(self._voltage)+'"'
        v_strjson += ',"intensite":"'+str(self._intensite)+'"'
        v_strjson += ',"compteur":"'+str(self._compteur)+'"'
        v_strjson += '}'
        return json.loads(v_strjson)

    def start(self):
        v_retour = "Success"
        user = b"admin"
        password = b"admin"
        try:
            tn = telnetlib.Telnet(self._ip)
            tn.read_until(b"login: ")
            tn.write(user + b"\n")
            if password:
                tn.read_until(b"Password: ")
                tn.write(password + b"\n")
            tn.write(b"GpioForCrond 1\n")
            tn.write(b"exit\n")
            response = tn.read_all()
            tn.close()
        except:
            v_retour = 'Failed'
        finally:
            return v_retour
    
    def stop(self):
        v_retour = "Success"
        user = b"admin"
        password = b"admin"
        try:
            tn = telnetlib.Telnet(self._ip)
            tn.read_until(b"login: ")
            tn.write(user + b"\n")
            if password:
                tn.read_until(b"Password: ")
                tn.write(password + b"\n")
            tn.write(b"GpioForCrond 0\n")
            tn.write(b"exit\n")
            response = tn.read_all()
            tn.close()
        except:
            v_retour = 'Failed'
        finally:
            return v_retour