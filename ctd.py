import requests
import re
import json
import os.path

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


def parseData():
    for key in datafiles:
        parsed_data = re.search('(\d{2}\.\d{2}.\d{4} \d{2}:\d{2})\D+(\d+\.\d{3}),(\d\.\d{3}),(\d\.\d{3})\r',
                                requests.get(datafiles[key]).text)
        if os.path.isfile(key + ".json"):
            with open(key + ".json", "r") as read_file:
                data_object = json.loads(read_file.read())

            append_data = {"date": parsed_data.group(1), "stauinhalt": parsed_data.group(2),
                           "zufluss": parsed_data.group(3),
                           "abfluss": parsed_data.group(4)}
            if append_data not in data_object["data"]:
                data_object["data"].append(append_data)
        else:
            data_object = {"name": key, "data": [
                {"date": parsed_data.group(1), "stauinhalt": parsed_data.group(2), "zufluss": parsed_data.group(3),
                 "abfluss": parsed_data.group(4)}]}

        with open(key + ".json", "w") as write_file:
            json.dump(data_object, write_file)


parseData()
