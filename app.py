import requests
from flask import Flask, render_template, request, jsonify

app = Flask(__name__)


API_KEY = "72982cc07057519a673d3fa3afb2041b"

def get_weather(city):
    try:
        
        url = f"http://api.openweathermap.org/data/2.5/weather?q={city}&appid={API_KEY}&units=metric"
        
        response = requests.get(url)
        data = response.json()

        if data["cod"] == 200:
            
            temp = data["main"]["temp"]
            desc = data["weather"][0]["description"].title()
            humidity = data["main"]["humidity"]
            wind = data["wind"]["speed"]
            city_name = data["name"]
            country = data["sys"]["country"]

            
            reply = (f"Current weather in <b>{city_name}, {country}</b>:<br>"
                     f"🌡️ <b>Temp:</b> {temp}°C<br>"
                     f"☁️ <b>Condition:</b> {desc}<br>"
                     f"💧 <b>Humidity:</b> {humidity}%<br>"
                     f"🍃 <b>Wind:</b> {wind} m/s")
            return reply
        else:
            return "Sorry, I couldn't find that city. Please check the spelling."
            
    except Exception as e:
        return "Sorry, there was a connection error."

@app.route("/")
def home():
    return render_template("index.html")

@app.route("/chat", methods=["POST"])
def chat():
    user_message = request.json.get("message")
    
    if not user_message:
        return jsonify({"response": "Please enter a city name."})

    # Call the weather function
    bot_response = get_weather(user_message)
    
    return jsonify({"response": bot_response})

if __name__ == "__main__":
    app.run(debug=True)