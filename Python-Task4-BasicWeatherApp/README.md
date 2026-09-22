# Basic Weather App

## OASIS INFOBYTE Python Programming Internship

### Task 4 — Basic Weather App

A desktop weather application built with Python and Tkinter that retrieves weather information from the OpenWeatherMap API.

## Features

* Search weather by city
* Current temperature
* Feels-like temperature
* Humidity
* Wind speed
* Current weather description
* Weather condition icon
* Forecast display
* Celsius and Fahrenheit toggle
* Network timeout handling
* Invalid API key handling
* City-not-found handling
* Empty city validation
* Weather errors displayed inside the GUI

## Technologies Used

* Python
* Tkinter
* Requests
* Pillow
* OpenWeatherMap API

## Installation

bash
python -m pip install requests pillow


## API Key Setup

The OpenWeatherMap API key is stored as an environment variable.

### PowerShell

powershell
$env:OPENWEATHER_API_KEY="YOUR_API_KEY"


Run the application:

powershell
python weather_app.py


## How to Use

1. Start the application.
2. Enter a city name.
3. Click **Get Weather**.
4. View the current weather information.
5. Use the Celsius/Fahrenheit button to change temperature units.
6. View the forecast information.

## Error Handling

The application handles:

* Empty city input
* City not found
* Invalid API key
* Network connection errors
* Network timeouts
* Weather service errors

## Security

The API key is supplied through an environment variable and is not stored in the Python source code or GitHub repository.

## Project Structure

text
Python-Task4-BasicWeatherApp/
├── weather_app.py
└── README.md

## API

Weather data is provided by OpenWeatherMap.

The application uses the OpenWeatherMap Current Weather API and forecast API.
