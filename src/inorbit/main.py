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




# Helper to compute geodetic coordinates from ECI
def eci_to_latlon(x, y, z):
    R = sqrt(x**2 + y**2 + z**2)
    lat = degrees(asin(z / R))
    lon = degrees(atan2(y, x))
    alt = R - 6371.0  # Approx Earth radius in km
    return lat, lon, alt

# Plot with Cartopy
def plot_trajectory(df):
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


if __name__ == "__main__":
    satellite_name = "ISS"

    # TLE lines for ISS (ZARYA)
    line1 = "1 25544U 98067A   25105.53237150  .00014782  00000+0  27047-3 0  9993"
    line2 = "2 25544  51.6375 257.3560 0005276  47.8113  31.7820 15.49569282505441"

    # Search for TLE data
    test_tle_search()

    # Load satellite
    sat = Satrec.twoline2rv(line1, line2)

    # Generate timestamps for 90 minutes at 1-minute intervals
    epoch_dt = sat_epoch_datetime(sat)
    timestamps = [epoch_dt + timedelta(minutes=i) for i in range(0, 91, 1)]

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
    plot_trajectory(df)


