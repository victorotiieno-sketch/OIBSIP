# Basic Weather App

## OASIS INFOBYTE Python Programming Internship

### Advanced Task 4 — Basic Weather App

A modern desktop weather dashboard built with Python and Tkinter. The application retrieves real-time weather information and forecast data from the OpenWeatherMap API and presents it through a multi-section graphical interface.

## Features

### Dashboard

* Real-time weather overview
* City and country display
* Current temperature
* Weather condition
* Weather condition icon
* Feels-like temperature
* Humidity
* Wind speed
* Atmospheric pressure
* Visibility
* Upcoming forecast overview
* Refresh weather data

### Weather

* Detailed current weather information
* Temperature
* Feels-like temperature
* Humidity
* Wind speed
* Atmospheric pressure
* Visibility
* Weather condition
* Country information

### Forecast

* Upcoming forecast information
* Next forecast periods
* 5-day forecast
* Daily temperature information
* Daily weather conditions

### Settings

* Celsius and Fahrenheit selection
* Temperature unit switching
* Location search information
* Application information

### Navigation

* Functional Dashboard section
* Functional Weather section
* Functional Forecast section
* Functional Settings section
* Active navigation indicator

### Search

* Search weather by city
* Enter key support
* Empty city validation
* City-not-found handling

### Error Handling

* Invalid API key handling
* City-not-found handling
* Network connection errors
* Network timeout errors
* Weather service errors
* Empty input validation

## Technologies Used

* Python
* Tkinter
* Requests
* Pillow
* OpenWeatherMap API

## Installation

Install the required Python packages:

bash
python -m pip install requests pillow


## API Key Setup

The OpenWeatherMap API key is supplied through an environment variable and is not stored in the Python source code.

### PowerShell

powershell
$env:OPENWEATHER_API_KEY="YOUR_API_KEY"


Run the application:

powershell
python weather_app.py


## How to Use

1. Start the application.
2. Enter a city name in the search field.
3. Click **Get Weather**.
4. Use the sidebar to navigate between Dashboard, Weather, Forecast, and Settings.
5. View current weather information on the Dashboard.
6. View detailed weather information under Weather.
7. View upcoming forecasts under Forecast.
8. Change the temperature unit from Settings or the °C/°F button.
9. Use Refresh to retrieve the latest weather information.

## Security

The API key is supplied through the `OPENWEATHER_API_KEY` environment variable.

The API key is not stored directly in the Python source code and should never be committed to the GitHub repository.

## Project Structure

text
Python-Task4-BasicWeatherApp/
├── weather_app.py
└── README.md


## API

Weather information is provided by OpenWeatherMap.

The application uses the OpenWeatherMap Current Weather API and 5-day/3-hour forecast API.

## Internship Task

**OASIS INFOBYTE Python Programming Internship**

**Track:** Python Programming

**Level:** Advanced

**Task:** Task 4 — Basic Weather App
