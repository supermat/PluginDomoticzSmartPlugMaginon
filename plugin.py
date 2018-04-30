# Basic Python Plugin Example
#
# Author: GizMoCuz
#
"""
<plugin key="SmartPlugMaginon" name="SmartPlug Maginon Plugin" author="supermat" version="1.0.0" wikilink="http://www.domoticz.com/wiki/plugins/plugin.html" externallink="https://matdomotique.wordpress.com">
 <params>
        <param field="Address" label="IP de la prise" width="400px" required="true" default="192.168.0.1"/>
        <param field="Mode6" label="Debug" width="75px">
            <options>
                <option label="True" value="Debug"/>
                <option label="False" value="Normal"  default="true" />
            </options>
        </param>
    </params>
</plugin>
"""
import Domoticz,datetime,json,pluginConfig,time
# from data import * #Pour le debug local sinon à mettre en commentaire
import maginon

class SmartPlugMaginonPlugin:
    enabled = False    
    _lastExecution = datetime.datetime.now()
    
    config = pluginConfig.pluginConfig()
    def __init__(self):
        #self.var = 123
        return

    def updateDeviceIfExist(self,  p_deviceType, p_deviceName, p_nValue, p_sValue):
        if self.config.isUnitExist(p_deviceType,p_deviceName):
            v_unitKey = self.config.getOrCreateUnitIdForDevice(p_deviceType,p_deviceName)
            if v_unitKey in Devices:
                # On ne met pas à jour un device de type deviceCommande s'il est déjà à jour
                if(p_deviceType.value != self.config.DeviceType.deviceCommande.value
                   or (p_deviceType.value == self.config.DeviceType.deviceCommande.value
                        and Devices[v_unitKey].sValue != p_sValue)
                ):
                    Devices[v_unitKey].Update(nValue=p_nValue, sValue=p_sValue)
                    Domoticz.Debug("Le dipositif de type "+p_deviceType.value +" associé à "+ p_deviceName + " a été mis à jour " + str(p_nValue) + "/" + str(p_sValue))
                else:
                    Domoticz.Debug("Le dipositif de type "+p_deviceType.value +" associé à "+ p_deviceName + " est déjà à jour.")
            else:
                Domoticz.Debug("Le dipositif de type "+p_deviceType.value +" associé à "+ p_deviceName + " a été supprimé dans Domoticz.")
        else:
            Domoticz.Debug("Le dipositif de type "+p_deviceType.value +" associé à "+ p_deviceName + " n'a pas été créé dans Domoticz. Veuillez désactiver et réactiver le plugin, en autorisant l'ajout de nouveaux dispositifs.")

    def updateSmartplugDevice(self):
        if self.config.isUnitExist(pluginConfig.pluginConfig.DeviceType.devicePuissance,str(self._ip)):
            m = maginon.Smartplug(self._ip)
            if(m.read()== "Success"):
                v_json = m.getInfo()
                Domoticz.Debug(json.dumps(v_json))
                v_sValue = str(v_json["puissance"])+";"+str(v_json["compteur"])
                self.updateDeviceIfExist(pluginConfig.pluginConfig.DeviceType.devicePuissance,str(self._ip),0,v_sValue)
                self.updateDeviceIfExist(pluginConfig.pluginConfig.DeviceType.deviceCommande,str(self._ip),int(v_json["etat"]),str(v_json["etat"]))
            else:
                Domoticz.Error("Erreur : A la mise à jour. Vérifier la prise ou l'adresse IP.")

    def onStart(self):
        Domoticz.Debug("onStart called")
        if Parameters["Mode6"] == "Debug":
            Domoticz.Debugging(1)
        self._ip = Parameters["Address"]
        if(self._ip == ""):
            Domoticz.Log("Veuillez renseigner une adresse IP.")
            return
        ## On vérifie que la prise réponde
        m = maginon.Smartplug(self._ip)
        if(m.read()== "Failed"):
            Domoticz.Error("Connexion impossible. La prise n'est pas connectée ou l'IP n'est pas bonne.")
            return
        # Création du device Puissance
        keyunit = self.config.getOrCreateUnitIdForDevice(pluginConfig.pluginConfig.DeviceType.devicePuissance,str(self._ip))
        if (keyunit not in Devices):
            v_dev = Domoticz.Device(Unit=keyunit, Name=self._ip, TypeName="kWh")
            v_dev.Create()
            Domoticz.Log("Création du dispositif "+self._ip)
        
        # Création du device Commande
        keyunit = self.config.getOrCreateUnitIdForDevice(pluginConfig.pluginConfig.DeviceType.deviceCommande,str(self._ip))
        if (keyunit not in Devices):
            v_dev = Domoticz.Device(Unit=keyunit, Name=self._ip, TypeName="Switch")
            v_dev.Create()
            Domoticz.Log("Création du dispositif "+self._ip)
        DumpConfigToLog()
        self.updateSmartplugDevice()

    def onStop(self):
        Domoticz.Log("onStop called")

    def onConnect(self, Connection, Status, Description):
        Domoticz.Log("onConnect called")

    def onMessage(self, Connection, Data, Status, Extra):
        Domoticz.Log("onMessage called")

    def onCommand(self, Unit, Command, Level, Hue):
        Domoticz.Debug("onCommand called for Unit " + str(Unit) + ": Parameter '" + str(Command) + "', Level: " + str(Level))
        # 2018-04-15 21:40:52.237 (SmartplugSalon) onCommand called for Unit 8: Parameter 'On', Level: 0
        # 2018-04-15 21:43:52.061 (SmartplugSalon) onCommand called for Unit 8: Parameter 'Off', Level: 0
        m = maginon.Smartplug(self._ip)
        if(str(Command) == "Off"):
            if(m.stop() == "Success"):
                self.updateDeviceIfExist(pluginConfig.pluginConfig.DeviceType.deviceCommande,str(self._ip),0,"0")
                time.sleep(2)
                self.updateSmartplugDevice()
            else:
                Domoticz.Error("Erreur : "+"onCommand called for Unit " + str(Unit) + ": Parameter '" + str(Command) + "', Level: " + str(Level))
        else:
            if(m.start() == "Success"):
                self.updateDeviceIfExist(pluginConfig.pluginConfig.DeviceType.deviceCommande,str(self._ip),1,"1")
                time.sleep(2)
                self.updateSmartplugDevice()
            else:
                Domoticz.Error("Erreur : "+"onCommand called for Unit " + str(Unit) + ": Parameter '" + str(Command) + "', Level: " + str(Level))

    def onNotification(self, Name, Subject, Text, Status, Priority, Sound, ImageFile):
        Domoticz.Log("Notification: " + Name + "," + Subject + "," + Text + "," + Status + "," + str(Priority) + "," + Sound + "," + ImageFile)

    def onDisconnect(self, Connection):
        Domoticz.Log("onDisconnect called")

    def onHeartbeat(self):
        Domoticz.Debug("onHeartbeat called")
        if self._lastExecution.minute == datetime.datetime.now().minute :
            return        
        self._lastExecution = datetime.datetime.now()
        if(self._ip == ""):
            Domoticz.Log("Veuillez renseigner une adresse IP.")
            return
        self.updateSmartplugDevice()

global _plugin
_plugin = SmartPlugMaginonPlugin()

def onStart():
    global _plugin
    _plugin.onStart()

def onStop():
    global _plugin
    _plugin.onStop()

def onConnect(Connection, Status, Description):
    global _plugin
    _plugin.onConnect(Connection, Status, Description)

def onMessage(Connection, Data, Status, Extra):
    global _plugin
    _plugin.onMessage(Connection, Data, Status, Extra)

def onCommand(Unit, Command, Level, Hue):
    global _plugin
    _plugin.onCommand(Unit, Command, Level, Hue)

def onNotification(Name, Subject, Text, Status, Priority, Sound, ImageFile):
    global _plugin
    _plugin.onNotification(Name, Subject, Text, Status, Priority, Sound, ImageFile)

def onDisconnect(Connection):
    global _plugin
    _plugin.onDisconnect(Connection)

def onHeartbeat():
    global _plugin
    _plugin.onHeartbeat()

    # Generic helper functions
def DumpConfigToLog():
    for x in Parameters:
        if Parameters[x] != "":
            Domoticz.Debug( "'" + x + "':'" + str(Parameters[x]) + "'")
    Domoticz.Debug("Device count: " + str(len(Devices)))
    for x in Devices:
        Domoticz.Debug("Device:           " + str(x) + " - " + str(Devices[x]))
        Domoticz.Debug("Device ID:       '" + str(Devices[x].ID) + "'")
        Domoticz.Debug("Device Name:     '" + Devices[x].Name + "'")
        Domoticz.Debug("Device nValue:    " + str(Devices[x].nValue))
        Domoticz.Debug("Device sValue:   '" + Devices[x].sValue + "'")
        Domoticz.Debug("Device LastLevel: " + str(Devices[x].LastLevel))
    return