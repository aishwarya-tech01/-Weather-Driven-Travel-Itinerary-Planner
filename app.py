import os
import requests
from flask import Flask, render_template, request

app = Flask(__name__)
app.secret_key = 'super_secret_weather_itinerary_key'

# 🔑 PASTE YOUR 32-CHARACTER OPENWEATHERMAP API KEY HERE:
API_KEY = 'YOUR_ACTUAL_API_KEY_HERE'

@app.route('/', methods=['GET', 'POST'])
def index():
    plan = None
    error_message = None
    
    if request.method == 'POST':
        city = request.form.get('city', '').strip()
        
        # Guard check to make sure the user didn't leave the placeholder text
        if API_KEY == 'YOUR_ACTUAL_API_KEY_HERE' or not API_KEY:
            error_message = "API Key missing! Please paste your real OpenWeatherMap key into app.py."
            return render_template('dashboard.html', plan=plan, error=error_message)
            
        # 1. Build the live API request web link
        url = f"http://api.openweathermap.org/data/2.5/weather?q={city}&appid={API_KEY}&units=metric"
        
        try:
            # 2. Send the background request to the weather cloud servers
            response = requests.get(url, timeout=10)
            weather_data = response.json()
            
            # 3. Process the response data based on the HTTP Status Code
            if response.status_code == 200:
                temp = round(weather_data['main']['temp'])
                desc = weather_data['weather'][0]['description'].capitalize()
                main_condition = weather_data['weather'][0]['main'].lower()
                
                # 🌤️ Custom rule-based itinerary system matching real-time forecasts
                if any(cond in main_condition for cond in ["rain", "drizzle", "thunderstorm", "snow"]):
                    activities = [
                        "☕ 09:00 AM - Hot filter coffee at a cozy indoor cafe",
                        "🏛️ 11:30 AM - Explore local historical indoor museum exhibits",
                        "📖 03:00 PM - Book hunting and reading at a historic covered library",
                        "🎭 07:00 PM - Attend an elegant indoor theatre drama production"
                    ]
                else:
                    activities = [
                        "🚶 08:30 AM - Morning historical walking tour through the old city",
                        "🧺 12:00 PM - Street food picnic in the central public gardens",
                        "📸 03:30 PM - Open-top hop-on sightseeing bus ride across major landmarks",
                        "🌅 06:30 PM - Relaxing sunset viewing from an outdoor panoramic terrace"
                    ]
                
                plan = {
                    'city': city.capitalize(),
                    'temp': temp,
                    'desc': desc,
                    'activities': activities
                }
            elif response.status_code == 401:
                error_message = "Invalid API Key! Your key might not be active yet (takes 30-120 mins) or has a typo."
            elif response.status_code == 404:
                error_message = f"City '{city}' not found! Please check your spelling and try again."
            else:
                error_message = f"Weather service error (Status Code: {response.status_code})."
                
        except requests.exceptions.RequestException:
            error_message = "Connection failed! Unable to reach the weather server. Please verify your internet connection."

    return render_template('dashboard.html', plan=plan, error=error_message)

if __name__ == '__main__':
    app.run(debug=True, use_reloader=False)