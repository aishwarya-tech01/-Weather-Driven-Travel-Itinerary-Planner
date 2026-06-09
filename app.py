import os
from flask import Flask, render_template, request

app = Flask(__name__)
app.secret_key = 'super_secret_weather_itinerary_key'

# ---- APPLICATION CORE LOGIC ENGINE ----

@app.route('/', methods=['GET', 'POST'])
def index():
    """
    Main routing channel. Handles initial page loads (GET) 
    and dynamic itinerary generation based on form inputs (POST).
    """
    plan = None
    
    if request.method == 'POST':
        # Retrieve and clean up the input city name from the form
        city = request.form.get('city', '').strip()
        
        # 🌤️ Rule-Based Condition Engine
        # (Simulating real-time API variations before linking external API keys)
        if "london" in city.lower() or "rain" in city.lower() or "paris" in city.lower():
            temp = 14
            desc = "Overcast & Rainy Mood"
            activities = [
                "☕ 09:00 AM - Hot filter coffee at a cozy indoor cafe",
                "🏛️ 11:30 AM - Explore local historical indoor museum exhibits",
                "📖 03:00 PM - Book hunting and reading at a historic covered library",
                "🎭 07:00 PM - Attend an elegant indoor theatre drama production"
            ]
        else:
            # Default fallback mode for sunny/clear weather profiles
            temp = 27
            desc = "Clear Sunny Sky"
            activities = [
                "🚶 08:30 AM - Morning historical walking tour through the old city",
                "🧺 12:00 PM - Street food picnic in the central public gardens",
                "📸 03:30 PM - Open-top hop-on sightseeing bus ride across major landmarks",
                "🌅 06:30 PM - Relaxing sunset viewing from an outdoor panoramic terrace"
            ]
            
        # Packaging data to sync seamlessly with the HTML parameters
        plan = {
            'city': city.capitalize(), 
            'temp': temp, 
            'desc': desc, 
            'activities': activities
        }
        
    # Renders your dedicated templates/dashboard.html file
    return render_template('dashboard.html', plan=plan)


# ---- MAIN CONTAINER RUN CHANNELS ----
if __name__ == '__main__':
    # Initialize the local web server container
    app.run(debug=True, use_reloader=False)