from flask import Flask, render_template, request
import requests
from datetime import datetime, timedelta

app = Flask(__name__)

WEATHER_KEY = "97fdc990d5ad61975eacbea9547cb148"
FLIGHT_KEY = "cebfb3a62ef5e0b59402e7ca184c707e"

ZIP = "49931,US"
AIRPORT = "CMX"

CAMERA_EMBED = "https://g1.ipcamlive.com/d20c1d26-cc9e-4c07-b443-41b003ffe823"


# ---------------- WEATHER ----------------
def get_weather():
    url = f"https://api.openweathermap.org/data/2.5/weather?zip={ZIP}&appid={WEATHER_KEY}&units=imperial"
    data = requests.get(url).json()
    print(data)
    
    return {
        "city": data["name"],
        "temp": data["main"]["temp"],
        "desc": data["weather"][0]["description"],
        "wind": data["wind"]["speed"]
    }


# ---------------- FLIGHTS ----------------
def get_flights(date):
    url = f"http://api.aviationstack.com/v1/flights?access_key={FLIGHT_KEY}&dep_iata={AIRPORT}&flight_date={date}"
    data = requests.get(url).json()

    arrivals = []
    departures = []

    for f in data.get("data", []):
        flight_info = {
            "airline": f.get("airline", {}).get("name", "N/A"),
            "flight": f.get("flight", {}).get("iata", "N/A"),
            "origin": f.get("departure", {}).get("airport", "N/A"),
            "destination": f.get("arrival", {}).get("airport", "N/A"),
            "scheduled": f.get("departure", {}).get("scheduled", "N/A"),
            "actual": f.get("departure", {}).get("actual", "N/A"),
            "status": f.get("flight_status", "N/A"),
            "gate": f.get("departure", {}).get("gate", "N/A")
        }

        # classify properly
        if f.get("flight_status") == "landed":
            arrivals.append(flight_info)
        else:
            departures.append(flight_info)

    return arrivals, departures


# ---------------- HOME ----------------
@app.route("/", methods=["GET", "POST"])
def home():

    selected_date = request.form.get("date") or datetime.now().strftime("%Y-%m-%d")

    weather = get_weather()

    arrivals, departures = get_flights(selected_date)

    today = datetime.now()
    past_2 = [(today - timedelta(days=i)).strftime("%Y-%m-%d") for i in range(1, 3)]
    tomorrow = (today + timedelta(days=1)).strftime("%Y-%m-%d")

    return render_template(
        "home.html",
        weather=weather,
        arrivals=arrivals[:5],
        departures=departures[:5],
        selected_date=selected_date,
        past_2=past_2,
        tomorrow=tomorrow,
        camera_embed=CAMERA_EMBED
    )

if __name__ == "__main__":
    app.run(debug=True)