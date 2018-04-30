# Domoticz Freebox Plugin
Plugin Python Domoticz pour l'utilisation d'un prise intelligente wifi Maginon
https://matdomotique.wordpress.com/2018/04/30/plugin-smartplug-maginon-pour-domoticz/

## Fonctionnalités

* Relevé de la puissance instantanée et de la consomation cumulée
* Interrupteur permettant l'allumage ou l'extinction de la prise. ATTENTION : l'état de la prise est simplement fonction de sa consommation instantanée. Si rien n'est connecté à la prise, il n'y aura aucune consommation, l'état de la prise remontera dans Domoticz comme éteinte même si celle ci est allumée. Pas mieux pour l'instant.

## Installation

Requis : Python version 3.4 or supérieur & Domoticz version 3.81xx ou supérieur.

* En ligne de commande aller dans le répertoire plugin de Domoticz (domoticz/plugins)
* Lancer la commande: ```git clone https://github.com/supermat/PluginDomoticzSmartPlugMaginon.git```
* Redémarrer le service Domoticz en lancant la commande ```sudo service domoticz.sh restart```

## Updating

Pour mettre à jour le plugin :

* En ligne de commande aller dans le répertoire plugin de Domoticz (domoticz/plugins)
* Lancer la commande: ```git pull```
* Redémarrer le service Domoticz en lancant la commande ```sudo service domoticz.sh restart```

## Configuration

| Field | Information|
| ----- | ---------- |
| Address | L'adresse IP de la prise sur le réseau local |
| Debug | Si true plus de log apparaitront dans la console de log |

Dans la partie Matériel de Domoticz, chercher 'Smartplug Maginon Plugin'.
Configurez l'adresse IP de la prise.
Ajoutez le Matériel et rendez vous dans les log.

| Dispositifs | Description|
| ----- | ---------- |
| Interrupteur | Interrupteur de commande on/off. L'état est fonction de la consommation (Si consommation > 0,2A prise on, sinon off)  |
| Compteur | Puissance instantannée et compteur cumulatif |

Note : Un fichier ```devicemapping.json``` est créé pour garder l'association des infos de la prise avec le bon device créé au moment du démarrage du Plugin.

## Change log

| Version | Information|
| ----- | ---------- |
| 1.0 | Version initial : consommation, puissance instantanée, commande On/Off |
