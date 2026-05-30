import google.generativeai as genai
import requests
import time

# Set up API keys
GEMINI_API_KEY = "AIzaSyCgcazA5TaXPTLTGOoQGvtC4x6w9DSeQNs"  # Replace with your actual Gemini API key
WEATHER_API_KEY = "3c3bbc5bc2392cce9b9ad50cdcec67f2"  # Replace with your actual Weather API key

# Configure Gemini AI
genai.configure(api_key=GEMINI_API_KEY)

# Function to get weather data based on location
def get_weather_data(city):
    print("\nFetching real-time weather data, please wait...")
    time.sleep(2)  # Simulating loading effect

    url = f"http://api.openweathermap.org/data/2.5/weather?q={city}&appid={WEATHER_API_KEY}&units=metric"
    response = requests.get(url)
    
    if response.status_code == 200:
        data = response.json()
        temperature = data["main"]["temp"]
        humidity = data["main"]["humidity"]
        rainfall = data.get("rain", {}).get("1h", 0)  # Rainfall in mm (last 1 hour)

        # Display fetched data
        print("\n--- Real-Time Weather Data ---")
        print(f"Temperature: {temperature}°C")
        print(f"Humidity: {humidity}%")
        print(f"Rainfall: {rainfall} mm")
        print("------------------------------")

        return temperature, humidity, rainfall
    else:
        print("\nError fetching weather data. Please check the city name or API key.")
        return None, None, None

# Function to get fertilizer recommendations
def get_fertilizer_recommendation():
    print("Select Environment Type:")
    print("1. Open Environment (Fetch Weather Data)")
    print("2. Closed Environment (Manual Input)")
    choice = input("Enter 1 or 2: ")

    if choice == "1":
        city = input("Enter your location (city name): ")
        temperature, humidity, rainfall = get_weather_data(city)

        if temperature is None:
            return  # Stop execution if weather data isn't available
    else:
        print("\nEnter manual environmental data:")
        temperature = input("Temperature (°C): ")
        humidity = input("Humidity (%): ")
        rainfall = input("Rainfall (mm): ")

    print("\nEnter soil and fertilizer details manually:")
    npk_values = input("Enter NPK ratio (e.g., 20-20-20): ")
    soil_moisture = input("Soil Moisture (%): ")

    # Create the prompt for AI
    prompt = f"""
    Given the following agricultural conditions:
    - Temperature: {temperature}°C
    - Humidity: {humidity}%
    - Rainfall: {rainfall} mm
    - Soil Moisture: {soil_moisture}%
    - NPK Ratio: {npk_values}

    Recommend the best fertilizer, application method, and precautions.
    """

    # Calling Gemini AI
    model = genai.GenerativeModel("models/gemini-1.5-pro")
    response = model.generate_content(prompt)

    # Display AI recommendation
    print("\n--- Recommended Fertilizer ---")
    print(response.text)

# Run the function
get_fertilizer_recommendation()
