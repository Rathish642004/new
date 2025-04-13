

🌤️ Real-Time Weather Web App

A dynamic Django web application that provides real-time weather updates for any location using the **OpenWeatherMap API**. Built with **Python**, **JavaScript**, **HTML**, and **CSS**, the app offers an intuitive interface and seamless data visualization.

🔧 Features

- 🌍 **Location-Based Weather Updates**: Enter any city to get the current weather data.
- 📡 **Real-Time API Integration**: Fetches data from [OpenWeatherMap](https://openweathermap.org/api) for accurate and up-to-date weather info.
- 📊 **Dynamic Data Visualization**: Displays temperature, humidity, wind speed, and weather conditions.
- 🖥️ **User-Friendly Interface**: Clean and responsive design for a smooth user experience.
- ⚠️ **Error Handling**: Displays meaningful error messages for invalid or empty location inputs.


## 🛠️ Tech Stack

- **Backend**: Django (Python)
- **Frontend**: HTML, CSS, JavaScript
- **API**: OpenWeatherMap API

---

## 🚀 Getting Started

1. **Clone the repository**
   ```bash
   git clone https://github.com/your-username/weather-web-app.git
   cd weather-web-app
   ```

2. **Set up a virtual environment**
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows use `venv\Scripts\activate`
   ```

3. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

4. **Set your OpenWeatherMap API key**

   - Create a `.env` file or add the key directly to `settings.py` as:
     ```python
     OPENWEATHER_API_KEY = "your_api_key_here"
     ```

5. **Run the server**
   ```bash
   python manage.py runserver
   ```

6. **Visit the app**
   Open `http://127.0.0.1:8000` in your browser.

---

## 📸 Screenshots

![image](https://github.com/user-attachments/assets/7bd63549-59a2-4a7b-a2cc-8836c9153f68)
