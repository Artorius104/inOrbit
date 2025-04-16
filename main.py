import requests
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from sgp4.api import Satrec, jday
from sgp4.conveniences import sat_epoch_datetime
from datetime import timedelta
from math import degrees, atan2, sqrt, asin
import cartopy.crs as ccrs
import cartopy.feature as cfeature


API_KEY="sJAxc5dCiOfv1ZRlISGgfTAG3nc8mOfngVXTAJUR"

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

# Usage example
def tle_search(name):
    satellites = search_tle_by_name(name)
    for sat in satellites:
        print(f"Nom: {sat['name']}")
        print(f"Date: {sat['date']}")
        print(f"Ligne 1: {sat['line1']}")
        print(f"Ligne 2: {sat['line2']}")
        print("-" * 50)

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


if __name__ == "__main__":
    satellite_name = "ISS"

    # TLE lines for ISS (ZARYA)
    line1 = "1 25544U 98067A   25105.53237150  .00014782  00000+0  27047-3 0  9993"
    line2 = "2 25544  51.6375 257.3560 0005276  47.8113  31.7820 15.49569282505441"

    # Search for TLE data
    tle_search(satellite_name)

    # Load satellite
    sat = Satrec.twoline2rv(line1, line2)

    # Generate timestamps for 90 minutes at 1-minute intervals
    epoch_dt = sat_epoch_datetime(sat)
    timestamps = [epoch_dt + timedelta(minutes=i) for i in range(0, 91, 1)]

    # Helper to compute geodetic coordinates from ECI
    def eci_to_latlon(x, y, z):
        R = sqrt(x**2 + y**2 + z**2)
        lat = degrees(asin(z / R))
        lon = degrees(atan2(y, x))
        alt = R - 6371.0  # Approx Earth radius in km
        return lat, lon, alt

    # Propagate and collect coordinates
    data = []
    for dt in timestamps:
        jd, fr = jday(dt.year, dt.month, dt.day, dt.hour, dt.minute, dt.second + dt.microsecond * 1e-6)
        e, r, v = sat.sgp4(jd, fr)
        if e == 0:
            lat, lon, alt = eci_to_latlon(*r)
            data.append({
                "datetime": dt.isoformat(),
                "latitude": lat,
                "longitude": lon,
                "altitude_km": alt
            })

    # Convert to DataFrame
    df = pd.DataFrame(data)

    # Save to CSV
    csv_path = "data/iss_trajectory_cartopy.csv"
    df.to_csv(csv_path, index=False)

    # Plot with Cartopy
    plt.figure(figsize=(12, 6))
    ax = plt.axes(projection=ccrs.PlateCarree())
    ax.set_global()
    ax.stock_img()
    ax.coastlines()
    ax.add_feature(cfeature.BORDERS, linestyle=':')
    ax.gridlines(draw_labels=True)

    # Plot the trajectory
    ax.plot(df["longitude"], df["latitude"], 'r-', marker='o', transform=ccrs.Geodetic())
    plt.title("Trajectoire de l'ISS (ZARYA) sur 90 minutes")
    plt.show()
