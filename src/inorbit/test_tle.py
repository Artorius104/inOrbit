import requests


# TLE (Two-Line Element set) est un format standard utilisé pour représenter les orbites des satellites artificiels.
def search_tle_by_name(name):
    url = f"https://tle.ivanstanojevic.me/api/tle?search={name}"
    headers = {"User-Agent": "Mozilla/5.0"}
    try:
        response = requests.get(url, headers=headers, timeout=10)
        response.raise_for_status()
        data = response.json()
        return data.get('member', [])
    except requests.exceptions.RequestException as e:
        print("Erreur de requête :", e)
        return []

def test_tle_search(name):
    satellites = search_tle_by_name(name)

    for sat in satellites:
        print(f"Nom: {sat['name']}")
        print(f"Date: {sat['date']}")
        print(f"Ligne 1: {sat['line1']}")
        print(f"Ligne 2: {sat['line2']}")
        print("-" * 50)

def main():
    satellite_name = "ISS"
    test_tle_search(satellite_name)


# Output example:
# Nom: ISS (ZARYA)
# Date: 2023-10-01
# Ligne 1: 1 25544U 98067A   23274.00000000  .00001234  00000-0  12345-6 0  9993
# Ligne 2: 2 25544  51.6456  23.4567 0001234 123.4567 234.5678 15.50123467890123 505441

# Signification des champs Ligne 1 :
# 1 :       Numéro de ligne
# 25544U :  NORAD ID, U = objet actif (vs "D" pour débris) 
# 98067A :  International Designator = Année 1998, 67e lancement, objet "A"
# 25105.53237150 : Époque au format "année julienne" → 2025, jour 105.532... (≈ 15 avril 2025 à 12h46 UTC)
# .00014782	: Premier dérivé du moyen mouvement = taux de variation de vitesse orbitale (accélération due aux perturbations)
# 00000+0 : Second dérivé du moyen mouvement (souvent 0)
# 27047-3 : Coefficient de freinage atmosphérique ("drag term", B*)
# 0 :       Numéro de type d’éphemeride (toujours 0 dans 99% des cas)
# 9993 :    Somme de contrôle (checksum, pour vérifier les erreurs)

# Signification des champs Ligne 2 :
# 2 :       Numéro de ligne
# 25544 :   NORAD ID
# 51.6456 : Inclinaison (inclination) en degrés
# 23.4567 : Ascension droite du nœud ascendant (RAAN) en degrés
# 0001234 : Excentricité (eccentricity) = 0.0001234
# 123.4567 : Argument du périgée (argument of perigee) en degrés
# 234.5678 : Anomalie moyenne (mean anomaly) en degrés
# 15.50123467890123 : Moyenne du mouvement (mean motion) en révolutions par jour
# 505441 :  Numéro de révolution depuis le lancement (approximatif)
