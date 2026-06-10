import requests

LAT = 54.16
LON = 11.95

def lade_windhistorie():

    url = (
        f"https://archive-api.open-meteo.com/v1/archive"
        f"?latitude={LAT}"
        f"&longitude={LON}"
        f"&past_days=3"
        f"&daily=wind_direction_10m_dominant"
        f"&timezone=Europe/Berlin"
    )

    response = requests.get(url)

    return response.json()

def windrichtung_text(grad):

    richtungen = [
        "N", "NO", "O", "SO",
        "S", "SW", "W", "NW"
    ]

    index = round(grad / 45) % 8

    return richtungen[index]




def bewerte_windhistorie(richtungen):

    if richtungen.count("NW") >= 3:
        return 15, "stabile NW-Lage"

    elif richtungen.count("W") >= 3:
        return 12, "stabile Westlage"

    elif richtungen.count("N") >= 3:
        return 10, "stabile Nordlage"

    elif richtungen.count("SW") >= 3:
        return 5, "überwiegend Südwest"

    elif richtungen.count("O") >= 2:
        return -10, "Ostwindphase"

    elif richtungen.count("SO") >= 2:
        return -15, "Südostwindphase"

    else:
        return 0, "wechselhafte Windlage"

    
def windhistorie_score():

    daten = lade_windhistorie()

    richtungen = []

    for grad in daten["daily"]["wind_direction_10m_dominant"]:

        richtungen.append(
            windrichtung_text(grad)
        )

    return bewerte_windhistorie(richtungen)

if __name__ == "__main__":

    daten = lade_windhistorie()

    richtungen = []

    for grad in daten["daily"]["wind_direction_10m_dominant"]:

        richtungen.append(
            windrichtung_text(grad)
        )

    print(richtungen)

    punkte, text = bewerte_windhistorie(richtungen)

    print(text)
    print(f"{punkte:+} Punkte")