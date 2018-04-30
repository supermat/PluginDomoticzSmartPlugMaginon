import json,os
from enum import Enum

class pluginConfig:
    class DeviceType(Enum):
        devicePuissance = 'Puissance'
        deviceCommande = 'Commande'
    
    _fileNameDeviceMapping = 'devicemapping.json'
    
    def __init__(self):
        return

    def getDicoUnitAllDevice(self):
        v_UnitKeyDico = {}
        if (os.path.isfile(self._fileNameDeviceMapping)):
                with open(self._fileNameDeviceMapping) as data_file:
                    v_UnitKeyDico = json.load(data_file)
        return v_UnitKeyDico

    def saveDicoUnitDevice(self, p_dicoToSave):
        with open(self._fileNameDeviceMapping, 'w', encoding='utf-8') as data_file:
                json.dump(p_dicoToSave, data_file)

    def getNextUnsuedUnit(self,p_dicoAll):
        v_count = 0
        for deviceType in p_dicoAll:
            v_count = v_count + len(p_dicoAll[deviceType])
        return v_count+1

    def getOrCreateUnitIdForDevice(self, p_deviceType, p_deviceName):
        # v_UnitKeyDico = self.getDicoUnitForDeviceType(p_deviceType)
        v_dicoAll = self.getDicoUnitAllDevice()
        if(p_deviceType.value in v_dicoAll):
            v_dicoDeviceType = v_dicoAll[p_deviceType.value]
        else:
            v_dicoDeviceType = {}
            v_dicoAll.update({p_deviceType.value:v_dicoDeviceType})
        if(p_deviceName in v_dicoDeviceType):
            return v_dicoDeviceType[p_deviceName]
        else:
            v_unit = self.getNextUnsuedUnit(v_dicoAll)
            v_dicoDeviceType.update({p_deviceName:v_unit})
            self.saveDicoUnitDevice(v_dicoAll)
            return v_unit
    
    def isUnitExist(self, p_deviceType, p_deviceName):
        v_dicoAll = self.getDicoUnitAllDevice()
        if(p_deviceType.value in v_dicoAll):
            v_dicoDeviceType = v_dicoAll[p_deviceType.value]
        else:
            return False
        if(p_deviceName in v_dicoDeviceType):
            return True
        else:
            return False

    