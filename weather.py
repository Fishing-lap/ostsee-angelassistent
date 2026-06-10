import requests

LAT = 54.16
LON = 11.95

def lade_wetterdaten():

    url = (
        f"https://api.open-meteo.com/v1/forecast"
        f"?latitude={LAT}"
        f"&longitude={LON}"
        f"&daily=temperature_2m_max,temperature_2m_min,"
        f"windspeed_10m_max,winddirection_10m_dominant"
        f"&timezone=Europe/Berlin"
    )

    response = requests.get(url)

    return response.json()

if __name__ == "__main__":
    daten = lade_wetterdaten()
    print(daten["daily"]["time"][0])