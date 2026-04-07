from flask import Flask, render_template
import requests

app = Flask(__name__)

API_KEY = "97fdc990d5ad61975eacbea9547cb148"
ZIP = "49931,US"

WEBCAM_URL = "https://g1.ipcamlive.com/d20c1d26-cc9e-4c07-b443-41b003ffe823"


@app.route("/")
def home():

    weather_url = f"https://api.openweathermap.org/data/2.5/weather?zip={ZIP}&appid={API_KEY}&units=imperial"
    weather_res = requests.get(weather_url)
    weather_data = weather_res.json()

    weather = {
        "city": weather_data["name"],
        "temp": weather_data["main"]["temp"],
        "description": weather_data["weather"][0]["description"],
        "wind": weather_data["wind"]["speed"]
    }

    forecast_url = f"https://api.openweathermap.org/data/2.5/forecast?zip={ZIP}&appid={API_KEY}&units=imperial"
    forecast_res = requests.get(forecast_url)
    forecast_data = forecast_res.json()

    forecast = []

    for item in forecast_data["list"][:8]:
        forecast.append({
            "time": item["dt_txt"],
            "temp": item["main"]["temp"],
            "description": item["weather"][0]["description"]
        })

    return render_template(
        "home.html",
        weather=weather,
        forecast=forecast,
        webcam_url=WEBCAM_URL
    )


if __name__ == "__main__":
    app.run(debug=True)