import os
import requests
from flask import Flask, render_template, request

app = Flask(__name__)
app.secret_key = 'super_secret_weather_itinerary_key'

# Keep empty for automated local simulation mode
API_KEY = ""

@app.route('/', methods=['GET', 'POST'])
def index():
    plan = None
    error_message = None

    if request.method == 'POST':
        # Safely grab the city from either the text input OR a bookmark button click
        city = request.form.get('city', '').strip()
        requested_days = int(request.form.get('days', 1))

        # Base templates for itinerary planning
        rainy_activities = [
            "☕ 09:00 AM - Hot filter coffee at an architectural indoor cafe",
            "🏛️ 11:30 AM - Explore local premium art museum exhibitions",
            "📖 03:00 PM - Book hunting inside a historic vaulted archive library",
            "🎭 07:00 PM - Attend an elegant indoor theatre musical performance"
        ]

        sunny_activities = [
            "🏃‍♂️ 08:30 AM - Guided history walking tour across the old city quarter",
            "🧺 12:00 PM - Local gourmet street-food picnic in the central botanical gardens",
            "🚌 03:30 PM - Open-top panoramic sightseeing bus ride across major landmarks",
            "🍹 06:30 PM - Sunset mocktails from an open-air viewpoint skyline lounge"
        ]

        # ---- LOCAL SIMULATION MODE ----
        if not API_KEY or API_KEY == 'YOUR_ACTUAL_API_KEY_HERE':
            is_rainy_profile = any(x in city.lower() for x in ["london", "paris", "rain", "pune", "mumbai"])
            
            temp = 14 if is_rainy_profile else 31
            desc = "Overcast Rain (Simulation Active)" if is_rainy_profile else "Clear Sunny Sky (Simulation Active)"
            main_condition = "rain" if is_rainy_profile else "clear"
            
            plan = build_itinerary_payload(city, temp, desc, main_condition, requested_days, rainy_activities, sunny_activities)
            return render_template('dashboard.html', plan=plan, error=None)

        # ---- LIVE API CONNECTOR ----
        url = f"http://api.openweathermap.org/data/2.5/weather?q={city}&appid={API_KEY}&units=metric"
        try:
            response = requests.get(url, timeout=6)
            weather_data = response.json()

            if response.status_code == 200:
                temp = round(weather_data['main']['temp'])
                desc = weather_data['weather'][0]['description'].capitalize()
                main_condition = weather_data['weather'][0]['main'].lower()
                plan = build_itinerary_payload(city, temp, desc, main_condition, requested_days, rainy_activities, sunny_activities)
            else:
                # Automatic fallback profile tracker if key is syncing
                is_rainy_profile = any(x in city.lower() for x in ["london", "paris", "rain", "pune", "mumbai"])
                temp = 14 if is_rainy_profile else 31
                desc = "Backup Profile Active (API Syncing)"
                main_condition = "rain" if is_rainy_profile else "clear"
                plan = build_itinerary_payload(city, temp, desc, main_condition, requested_days, rainy_activities, sunny_activities)

        except requests.exceptions.RequestException:
            error_message = "Network timeout. Switched to standby layout mode."

    return render_template('dashboard.html', plan=plan, error=error_message)


def build_itinerary_payload(city, temp, desc, main_condition, days, rainy_acts, sunny_acts):
    """
    Assembles the backend structural parameters, packing tips, 
    calculated budgets, and dynamic mood playlists seamlessly.
    """
    # Define a flat base cost per day in USD for our budget calculations
    base_daily_cost = 75

    # 🌧️ Feature: Check if weather is Rainy or Stormy
    if any(cond in main_condition for cond in ["rain", "drizzle", "thunderstorm", "snow"]):
        icon = "🌧️"
        bg_color = "#0b1329"          
        accent_color = "#f43f5e"      
        packing_list = ["☔ Compact Umbrella", "🧥 Waterproof Raincoat", "🥾 Non-slip Boots"]
        selected_activities = rainy_acts
        
        # New Feature: Dynamic Rainy Mood Suggestions
        mood_quote = "🎵 Cozy Rain Vibe: Perfect time to grab a hot drink, listen to some chill low-fi beats, and explore indoor spots!"
        
    # ☀️ Otherwise assume clear/sunny parameters
    else:
        icon = "☀️"
        bg_color = "#1c1917"          
        accent_color = "#eab308"      
        packing_list = ["🕶️ Sunglasses", "🧴 Sunscreen SPF 50+", "🥤 Hydration Flask"]
        selected_activities = sunny_acts
        
        # New Feature: Dynamic Sunny Mood Suggestions
        mood_quote = "🎵 Sunny Adventure Vibe: Cue up an upbeat road-trip anthem and get ready to catch an outdoor sunset viewpoint!"

    # New Feature: Mathematical Budget Calculation (Days * Daily Cost)
    estimated_budget = days * base_daily_cost

    return {
        'city': city.capitalize(),
        'temp': temp,
        'desc': desc,
        'icon': icon,
        'bg_color': bg_color,
        'accent_color': accent_color,
        'packing_list': packing_list,
        'activities_by_day': selected_activities,
        'total_days': days,
        'mood_quote': mood_quote,             # Sent down to frontend template
        'estimated_budget': estimated_budget  # Total numeric cost processed
    }

if __name__ == '__main__':
    app.run(debug=True, use_reloader=False)