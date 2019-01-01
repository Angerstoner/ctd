import requests
import re
import json
import os.path
from datetime import datetime

datafiles = {
    "Ecker": "http://talis.harzwasserwerke.de/talsperren/talis/eck_tab.txt",
    "Grane": "http://talis.harzwasserwerke.de/talsperren/talis/gra_tab.txt",
    "Innerste": "http://talis.harzwasserwerke.de/talsperren/talis/inn_tab.txt",
    "Oder": "http://talis.harzwasserwerke.de/talsperren/talis/ode_tab.txt",
    "Oker": "http://talis.harzwasserwerke.de/talsperren/talis/oke_tab.txt",
    "Soese": "http://talis.harzwasserwerke.de/talsperren/talis/soes_tab.txt"
}

max_stau_data = {
    "Ecker": 13.27,
    "Grane": 46.4,
    "Innerste": 19.26,
    "Oder": 30.61,
    "Oker": 46.85,
    "Soese": 25.6
}


def unix_time_millis(dt):
    epoch = datetime.utcfromtimestamp(0)
    return int((dt - epoch).total_seconds() * 1000.0)


def parse_data():
    for key in datafiles:
        print(key)
        raw_data = requests.get(datafiles[key]).text.splitlines()
        for line in raw_data:
            if "24:" in line:
                line = line.replace("24:", "00:")

            if line != "":
                parsed_data = re.search('(\d{2}\.\d{2}.\d{4} \d{2}:\d{2})\D+(\d+\.\d{3}),(\d+\.\d{3}),(\d+\.\d{3})',
                                        line)
                unformatted_date, stauinhalt, zufluss, abfluss = parsed_data.groups()
                date = unix_time_millis(datetime.strptime(unformatted_date, '%d.%m.%Y %H:%M'))
                fuellgrad = round(float(stauinhalt) / max_stau_data[key] * 100, 2)

                if os.path.isfile("static/" + key + ".json"):
                    with open("static/" + key + ".json", "r") as read_file:
                        data_object = json.loads(read_file.read())

                    append_data = {"date": date,
                                   "stauinhalt": float(stauinhalt),
                                   "fuellgrad": fuellgrad,
                                   "zufluss": float(zufluss),
                                   "abfluss": float(abfluss)}

                    if append_data not in data_object["data"]:
                        data_object["data"].append(append_data)
                else:
                    data_object = {"name": key,
                                   "max. stauinhalt": max_stau_data[key],
                                   "data": [
                                       {"date": date,
                                        "stauinhalt": float(stauinhalt),
                                        "fuellgrad": fuellgrad,
                                        "zufluss": float(zufluss),
                                        "abfluss": float(abfluss)}]
                                   }

                data_object["data"].sort(key=lambda k: k['date'])
                with open("static/" + key + ".json", "w") as write_file:
                    json.dump(data_object, write_file)


parse_data()
