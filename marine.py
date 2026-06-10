import requests

LAT = 54.16
LON = 11.95

def lade_marine_daten():

    marine_url = (
        f"https://marine-api.open-meteo.com/v1/marine"
        f"?latitude={LAT}"
        f"&longitude={LON}"
        f"&daily=wave_height_max"
        f"&timezone=Europe/Berlin"
    )

    response = requests.get(marine_url)

    return response.json()

if __name__ == "__main__":
    daten = lade_marine_daten()
    print(daten["daily"]["wave_height_max"][0])