import os
import io
import requests
import tkinter as tk
from tkinter import ttk, messagebox
from PIL import Image, ImageTk


API_KEY = os.getenv("OPENWEATHER_API_KEY")


class WeatherApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Weather App")
        self.root.geometry("900x750")
        self.root.resizable(False, False)

        self.unit = "metric"
        self.unit_symbol = "°C"
        self.current_data = None
        self.forecast_data = None

        self.build_interface()

    def build_interface(self):
        title = tk.Label(
            self.root,
            text="Weather App",
            font=("Arial", 24, "bold")
        )
        title.pack(pady=15)

        search_frame = tk.Frame(self.root)
        search_frame.pack(pady=5)

        self.city_entry = tk.Entry(
            search_frame,
            width=35,
            font=("Arial", 13)
        )
        self.city_entry.grid(row=0, column=0, padx=5)

        self.city_entry.insert(0, "Kisumu")

        get_button = tk.Button(
            search_frame,
            text="Get Weather",
            font=("Arial", 11, "bold"),
            command=self.get_weather
        )
        get_button.grid(row=0, column=1, padx=5)

        self.unit_button = tk.Button(
            search_frame,
            text="Switch to °F",
            command=self.toggle_unit
        )
        self.unit_button.grid(row=0, column=2, padx=5)

        self.status_label = tk.Label(
            self.root,
            text="Enter a city and click Get Weather",
            font=("Arial", 10)
        )
        self.status_label.pack(pady=5)

        self.current_frame = tk.LabelFrame(
            self.root,
            text="Current Weather",
            font=("Arial", 12, "bold"),
            padx=15,
            pady=10
        )
        self.current_frame.pack(fill="x", padx=20, pady=10)

        self.current_info = tk.Label(
            self.current_frame,
            text="No weather data",
            font=("Arial", 13),
            justify="left"
        )
        self.current_info.pack(side="left", padx=20)

        self.icon_label = tk.Label(self.current_frame)
        self.icon_label.pack(side="right", padx=30)

        hourly_frame = tk.LabelFrame(
            self.root,
            text="Next 6 Hours",
            font=("Arial", 12, "bold"),
            padx=10,
            pady=10
        )
        hourly_frame.pack(fill="x", padx=20, pady=10)

        self.hourly_tree = ttk.Treeview(
            hourly_frame,
            columns=("time", "temperature", "condition"),
            show="headings",
            height=4
        )

        self.hourly_tree.heading("time", text="Time")
        self.hourly_tree.heading("temperature", text="Temperature")
        self.hourly_tree.heading("condition", text="Condition")

        self.hourly_tree.column("time", width=180)
        self.hourly_tree.column("temperature", width=180)
        self.hourly_tree.column("condition", width=300)

        self.hourly_tree.pack(fill="x")

        daily_frame = tk.LabelFrame(
            self.root,
            text="5-Day Forecast",
            font=("Arial", 12, "bold"),
            padx=10,
            pady=10
        )
        daily_frame.pack(fill="x", padx=20, pady=10)

        self.daily_tree = ttk.Treeview(
            daily_frame,
            columns=("date", "temperature", "condition"),
            show="headings",
            height=5
        )

        self.daily_tree.heading("date", text="Date")
        self.daily_tree.heading("temperature", text="Temperature")
        self.daily_tree.heading("condition", text="Condition")

        self.daily_tree.column("date", width=180)
        self.daily_tree.column("temperature", width=180)
        self.daily_tree.column("condition", width=300)

        self.daily_tree.pack(fill="x")

    def get_weather(self):
        city = self.city_entry.get().strip()

        if not city:
            self.show_error("Please enter a city.")
            return

        if not API_KEY:
            self.show_error(
                "OpenWeather API key is not configured.\n\n"
                "Set the OPENWEATHER_API_KEY environment variable "
                "and restart the application."
            )
            return

        self.status_label.config(text="Loading weather...")
        self.root.update_idletasks()

        try:
            current_url = (
                "https://api.openweathermap.org/data/2.5/weather"
                f"?q={city}&appid={API_KEY}&units={self.unit}"
            )

            forecast_url = (
                "https://api.openweathermap.org/data/2.5/forecast"
                f"?q={city}&appid={API_KEY}&units={self.unit}"
            )

            current_response = requests.get(
                current_url,
                timeout=10
            )

            forecast_response = requests.get(
                forecast_url,
                timeout=10
            )

            if current_response.status_code == 401:
                self.show_error("Invalid or inactive API key.")
                return

            if current_response.status_code == 404:
                self.show_error("City not found.")
                return

            if current_response.status_code != 200:
                self.show_error(
                    f"Weather service error: {current_response.status_code}"
                )
                return

            if forecast_response.status_code != 200:
                self.show_error(
                    f"Forecast service error: {forecast_response.status_code}"
                )
                return

            self.current_data = current_response.json()
            self.forecast_data = forecast_response.json()

            self.display_current_weather()
            self.display_hourly_forecast()
            self.display_daily_forecast()

            self.status_label.config(
                text=f"Weather loaded for {self.current_data['name']}, "
                     f"{self.current_data['sys']['country']}"
            )

        except requests.exceptions.Timeout:
            self.show_error(
                "The weather service timed out. Please try again."
            )

        except requests.exceptions.ConnectionError:
            self.show_error(
                "Unable to connect to the weather service."
            )

        except requests.exceptions.RequestException:
            self.show_error(
                "A network error occurred."
            )

        except Exception as error:
            self.show_error(
                f"An unexpected error occurred:\n{error}"
            )

    def display_current_weather(self):
        data = self.current_data

        temperature = data["main"]["temp"]
        feels_like = data["main"]["feels_like"]
        humidity = data["main"]["humidity"]
        wind = data["wind"]["speed"]
        description = data["weather"][0]["description"]
        icon_code = data["weather"][0]["icon"]

        text = (
            f"Location: {data['name']}, {data['sys']['country']}\n"
            f"Temperature: {temperature:.1f}{self.unit_symbol}\n"
            f"Feels Like: {feels_like:.1f}{self.unit_symbol}\n"
            f"Condition: {description.title()}\n"
            f"Humidity: {humidity}%\n"
            f"Wind Speed: {wind} m/s"
        )

        self.current_info.config(text=text)

        self.load_weather_icon(icon_code)

    def load_weather_icon(self, icon_code):
        try:
            url = (
                f"https://openweathermap.org/img/wn/"
                f"{icon_code}@2x.png"
            )

            response = requests.get(url, timeout=10)
            image = Image.open(io.BytesIO(response.content))
            image = image.resize((100, 100))

            self.weather_icon = ImageTk.PhotoImage(image)
            self.icon_label.config(image=self.weather_icon)

        except Exception:
            self.icon_label.config(image="")

    def display_hourly_forecast(self):
        for item in self.hourly_tree.get_children():
            self.hourly_tree.delete(item)

        entries = self.forecast_data["list"][:2]

        for item in entries:
            time_text = item["dt_txt"]
            temperature = item["main"]["temp"]
            condition = item["weather"][0]["description"].title()

            self.hourly_tree.insert(
                "",
                "end",
                values=(
                    time_text,
                    f"{temperature:.1f}{self.unit_symbol}",
                    condition
                )
            )

    def display_daily_forecast(self):
        for item in self.daily_tree.get_children():
            self.daily_tree.delete(item)

        days = {}

        for item in self.forecast_data["list"]:
            date = item["dt_txt"].split(" ")[0]

            if date not in days:
                days[date] = []

            days[date].append(item)

        dates = list(days.keys())[:5]

        for date in dates:
            entries = days[date]

            temperatures = [
                entry["main"]["temp"]
                for entry in entries
            ]

            conditions = [
                entry["weather"][0]["description"]
                for entry in entries
            ]

            average_temperature = sum(temperatures) / len(temperatures)

            condition = max(
                set(conditions),
                key=conditions.count
            )

            self.daily_tree.insert(
                "",
                "end",
                values=(
                    date,
                    f"{average_temperature:.1f}{self.unit_symbol}",
                    condition.title()
                )
            )

    def toggle_unit(self):
        if self.unit == "metric":
            self.unit = "imperial"
            self.unit_symbol = "°F"
            self.unit_button.config(text="Switch to °C")
        else:
            self.unit = "metric"
            self.unit_symbol = "°C"
            self.unit_button.config(text="Switch to °F")

        if self.current_data:
            self.get_weather()

    def show_error(self, message):
        self.status_label.config(text="Error")
        messagebox.showerror("Weather App", message)


if __name__ == "__main__":
    root = tk.Tk()
    app = WeatherApp(root)
    root.mainloop()