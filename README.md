# 🌍 Weather-Driven Travel Itinerary Planner

A smart travel companion web application built using **Python**, **Flask**, and **SQLite3**. The application connects directly to a live global weather forecast API to dynamically generate a customized day-by-day travel itinerary based on the current climate of the destination city.

---

## 🌟 Core Application Features

1. **Live Weather API Integration**
   * Uses Python's `requests` library to fetch live, real-time weather stats (temperature, rain status, UV index) from a public REST API (like OpenWeatherMap).
2. **Conditional Smart Recommendation Engine**
   * Automatically calculates and adapts travel schedules on the fly:
     * ☀️ **Sunny Days:** Recommends outdoor historical walks, beaches, and sightseeing.
     * 🌧️ **Rainy Days:** Automatically switches recommendations to indoor museums, cafes, and art galleries.
3. **Local Travel History Ledger**
   * Built-in SQLite3 storage keeps a permanent log of your planned itineraries so you can review them later

---

## ⚙️ Tech Stack & Concepts Covered

* **Backend Engine:** Python 3.x with Flask (handles route management and API payload parsing)
* **Database Management:** SQLite3 (stores saved destination spots and custom user itineraries).
* **Network Communication:** External API data fetching via the HTTP `requests` module
* **Frontend Design:** HTML5 / CSS3 structured dashboard.

---

## 🛠️ Step-by-Step Local Setup Guide

Follow these simple terminal commands to run this project locally on your computer:

### 1. Install Necessary Python Packages
Open your terminal in VS Code and install the web framework and networking packages:
```bash
pip install Flask requests
