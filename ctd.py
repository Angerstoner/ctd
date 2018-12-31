import requests
import re

datakeys = {
    "name": "talsperrenname",
    "zufluss": "data_zufluss",
    "stauinhalt": "data_stauinhalt",
    "uw-abgabe": "data_uwabgabe",
    "max_stauinhalt": "data_stauhoehe",
    "fuellungsgrad": "fuellungsgrad"
}

datafiles = {
    "Ecker": "http://talis.harzwasserwerke.de/talsperren/talis/eck_tab.txt",
    "Grane": "http://talis.harzwasserwerke.de/talsperren/talis/gra_tab.txt",
    "Innerste": "http://talis.harzwasserwerke.de/talsperren/talis/inn_tab.txt",
    "Oder": "http://talis.harzwasserwerke.de/talsperren/talis/ode_tab.txt",
    "Oker": "http://talis.harzwasserwerke.de/talsperren/talis/oke_tab.txt",
    "Soese": "http://talis.harzwasserwerke.de/talsperren/talis/soes_tab.txt"
}

parsedData = {
}

def parseData():
    for key in datafiles:
        parsedData[key] = re.search('(.*)\r', requests.get(datafiles[key]).text).group(1)
    print(parsedData)


parseData()
