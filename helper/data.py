import requests, json, config
from deepdiff import DeepDiff
from utils.logger import logs

def check_splatoon3_data(path: str = "./data/s3/translation.json") -> None:
    try:
        reponse = requests.get(f"{config.SPLATOON3_API}/locale/fr-FR.json", headers = config.HEADERS_BASE, timeout = config.TIMEOUT)
    except requests.Timeout:
        logs.fail("Impossible de vérifier si le fichier de traduction doit être mis à jour", "[UPDATE]")
        return
    
    if reponse.status_code == 200:
        reponse_json   = reponse.json()
        splatoon3_data = json.load(open(path))

        if DeepDiff(splatoon3_data, reponse_json, ignore_string_case = True) != {}:
            logs.warning('Le fichier "translation.json" de Splatoon 3 nécessite une mise à jour', "[UPDATE]")
            with open(path, "w") as json_file:
                json_file.write(json.dumps(reponse_json))
                logs.success('Mise à jour du fichier "translation.json" de Splatoon 3 réussis avec succès', "[UPDATE]")