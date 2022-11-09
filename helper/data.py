import requests, json, config
from deepdiff import DeepDiff
from utils.logger import logs

def check_splatoon3_data() -> None:
    reponse = requests.get(config.SPLATOON3_API + "/locale/fr-FR.json", headers = config.HEADERS_BASE)
    if reponse.status_code == 200:
        reponse_json   = reponse.json()
        splatoon3_data = json.load(open("./data/splatoon3.json"))

        if DeepDiff(splatoon3_data, reponse_json, ignore_string_case = True) != {}:
            logs.warning('Le fichier "splatoon3.json" nécessite une mise à jour', "[UPDATE]")
            with open('./data/splatoon3.json', "w") as json_file:
                json_file.write(json.dumps(reponse_json))
                logs.success("Mise à jour du fichier Splatoon3.json réussis avec succès", "[UPDATE]")