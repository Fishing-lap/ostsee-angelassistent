from weather import lade_wetterdaten
from marine import lade_marine_daten
from windhistory import windhistorie_score

LAT = 54.16
LON = 11.95

url = (
    f"https://api.open-meteo.com/v1/forecast"
    f"?latitude={LAT}"
    f"&longitude={LON}"
    f"&daily=temperature_2m_max,temperature_2m_min,"
    f"windspeed_10m_max,winddirection_10m_dominant"
    f"&timezone=Europe/Berlin"
)

data = lade_wetterdaten()
marine_data = lade_marine_daten()

marine_url = (
    f"https://marine-api.open-meteo.com/v1/marine"
    f"?latitude={LAT}"
    f"&longitude={LON}"
    f"&daily=wave_height_max"
    f"&timezone=Europe/Berlin"
)



print("Angelwetter Nienhagen")
print("-" * 50)

daily = data["daily"]

tage = []

def windrichtung_text(grad):
    richtungen = [
        "N", "NO", "O", "SO",
        "S", "SW", "W", "NW"
    ]

    index = round(grad / 45) % 8
    return richtungen[index]

for i in range(len(daily["time"])):

    wind = daily["windspeed_10m_max"][i]

    richtung_grad = daily["winddirection_10m_dominant"][i]
    richtung = windrichtung_text(richtung_grad)

    wellen = marine_data["daily"]["wave_height_max"][i]

    score = 50
    gruende = []

    # Windbewertung
    if wind <= 20:
        score += 25
        gruende.append("moderate Windstärke")
    elif wind <= 30:
        score += 10
        gruende.append("noch gut befischbarer Wind")
    else:
        score -= 15
        gruende.append("starker Wind")

    # Wellenbewertung
    if wellen < 0.3:
        score -= 10
        gruende.append("zu wenig Wasserbewegung")
    elif 0.3 <= wellen <= 0.8:
        score += 20
        gruende.append("optimale Wellenhöhe")
    elif 0.8 < wellen <= 1.2:
        score += 10
        gruende.append("gute Wellenhöhe")
    elif wellen > 1.5:
        score -= 20
        gruende.append("sehr hohe Wellen")

    # Richtungsbewertung
    if richtung == "NW":
        score += 15
        gruende.append("NW-Wind")
    elif richtung == "W":
        score += 10
        gruende.append("Westwind")
    elif richtung == "N":
        score += 8
        gruende.append("Nordwind")
    elif richtung == "SW":
        score += 5
        gruende.append("Südwestwind")
    elif richtung == "NO":
        score += 5
        gruende.append("Nordostwind")
    elif richtung == "O":
        score -= 10
        gruende.append("Ostwind")
    elif richtung == "SO":
        score -= 15
        gruende.append("Südostwind")
    elif richtung == "S":
        score -= 5
        gruende.append("Südwind")

    score = min(score, 100)

    if score >= 90:
        bewertung = "TOP-TAG"
    elif score >= 75:
        bewertung = "SEHR GUT"
    elif score >= 60:
        bewertung = "GUT"
    elif score >= 40:
        bewertung = "MITTEL"
    else:
        bewertung = "SCHWACH"

    punkte_hist, text_hist = windhistorie_score()

    score += punkte_hist
    gruende.append(text_hist)

    tage.append({
        "datum": daily["time"][i],
        "score": score,
        "bewertung": bewertung,
        "gruende": gruende.copy()
})

    print(
        f"{daily['time'][i]} | "
        f"Wind {wind} km/h | "
        f"{richtung} | "
        f"Wellen {wellen} m | "
        f"Score {score}/100 | "
        f"{bewertung}"
    )

    print()
print("=" * 50)
print("TOP 3 ANGELTAGE")
print("=" * 50)

top_tage = sorted(
    tage,
    key=lambda tag: tag["score"],
    reverse=True
)

for platz, tag in enumerate(top_tage[:3], start=1):

    print()
    print(
        f"{platz}. {tag['datum']} | "
        f"{tag['score']}/100 | "
        f"{tag['bewertung']}"
    )

    print("Gründe:")

    for grund in tag["gruende"]:
        print(f"  - {grund}")