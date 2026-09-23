import os
import io
import requests
import tkinter as tk
from tkinter import messagebox
from datetime import datetime
from collections import Counter
from PIL import Image, ImageTk


class WeatherApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Weatherly")
        self.root.geometry("1250x820")
        self.root.minsize(1100, 750)
        self.root.configure(bg="#0b1220")

        self.colors = {
            "bg": "#0b1220",
            "sidebar": "#111a2b",
            "card": "#162238",
            "card2": "#1b2941",
            "input": "#202f47",
            "primary": "#4f8cff",
            "primary_light": "#72a7ff",
            "text": "#f8fafc",
            "muted": "#91a0b8",
            "border": "#263751",
            "green": "#4ade80",
            "red": "#f87171"
        }

        self.unit = "metric"
        self.unit_symbol = "°C"
        self.current_data = None
        self.forecast_data = None
        self.current_icon = None
        self.forecast_images = []
        self.nav_buttons = {}

        self.build_interface()

    def build_interface(self):
        self.sidebar = tk.Frame(
            self.root,
            bg=self.colors["sidebar"],
            width=220
        )
        self.sidebar.pack(side="left", fill="y")
        self.sidebar.pack_propagate(False)

        self.content = tk.Frame(
            self.root,
            bg=self.colors["bg"]
        )
        self.content.pack(
            side="right",
            fill="both",
            expand=True
        )

        self.build_sidebar()
        self.build_content()

    def build_sidebar(self):
        logo = tk.Frame(
            self.sidebar,
            bg=self.colors["sidebar"]
        )
        logo.pack(
            fill="x",
            padx=22,
            pady=(30, 45)
        )

        tk.Label(
            logo,
            text="☁",
            bg=self.colors["primary"],
            fg="white",
            font=("Segoe UI", 20, "bold"),
            width=2
        ).pack(side="left")

        tk.Label(
            logo,
            text="Weatherly",
            bg=self.colors["sidebar"],
            fg=self.colors["text"],
            font=("Segoe UI Semibold", 17)
        ).pack(
            side="left",
            padx=10
        )

        self.create_nav_button(
            "Dashboard",
            "⌂",
            self.show_dashboard
        )

        self.create_nav_button(
            "Weather",
            "☀",
            self.show_weather
        )

        self.create_nav_button(
            "Forecast",
            "◷",
            self.show_forecast
        )

        self.create_nav_button(
            "Settings",
            "⚙",
            self.show_settings
        )

        spacer = tk.Frame(
            self.sidebar,
            bg=self.colors["sidebar"]
        )
        spacer.pack(fill="both", expand=True)

        info = tk.Frame(
            self.sidebar,
            bg=self.colors["card"]
        )
        info.pack(
            fill="x",
            padx=18,
            pady=20
        )

        tk.Label(
            info,
            text="WEATHER APP",
            bg=self.colors["card"],
            fg=self.colors["primary_light"],
            font=("Segoe UI Semibold", 9)
        ).pack(
            anchor="w",
            padx=15,
            pady=(15, 5)
        )

        tk.Label(
            info,
            text="Real-time weather\npowered by OpenWeatherMap",
            bg=self.colors["card"],
            fg=self.colors["muted"],
            justify="left",
            font=("Segoe UI", 9)
        ).pack(
            anchor="w",
            padx=15,
            pady=(0, 15)
        )

    def create_nav_button(self, name, icon, command):
        button = tk.Frame(
            self.sidebar,
            bg=self.colors["sidebar"],
            height=48,
            cursor="hand2"
        )
        button.pack(
            fill="x",
            padx=12,
            pady=4
        )

        icon_label = tk.Label(
            button,
            text=icon,
            bg=self.colors["sidebar"],
            fg=self.colors["muted"],
            font=("Segoe UI", 15),
            width=3,
            cursor="hand2"
        )
        icon_label.pack(side="left")

        text_label = tk.Label(
            button,
            text=name,
            bg=self.colors["sidebar"],
            fg=self.colors["muted"],
            font=("Segoe UI", 10),
            cursor="hand2"
        )
        text_label.pack(side="left")

        for widget in (button, icon_label, text_label):
            widget.bind(
                "<Button-1>",
                lambda event, action=command: action()
            )

        self.nav_buttons[name] = (
            button,
            icon_label,
            text_label
        )

    def set_active(self, name):
        for button_name, widgets in self.nav_buttons.items():
            button, icon, label = widgets

            if button_name == name:
                bg = self.colors["primary"]
                fg = "white"
                font = ("Segoe UI Semibold", 10)
            else:
                bg = self.colors["sidebar"]
                fg = self.colors["muted"]
                font = ("Segoe UI", 10)

            button.config(bg=bg)
            icon.config(
                bg=bg,
                fg=fg
            )
            label.config(
                bg=bg,
                fg=fg,
                font=font
            )

    def build_content(self):
        self.header = tk.Frame(
            self.content,
            bg=self.colors["bg"]
        )
        self.header.pack(
            fill="x",
            padx=35,
            pady=(28, 18)
        )

        title_area = tk.Frame(
            self.header,
            bg=self.colors["bg"]
        )
        title_area.pack(side="left")

        self.page_title = tk.Label(
            title_area,
            text="Weather Dashboard",
            bg=self.colors["bg"],
            fg=self.colors["text"],
            font=("Segoe UI Semibold", 23)
        )
        self.page_title.pack(anchor="w")

        self.page_subtitle = tk.Label(
            title_area,
            text="Monitor current conditions and upcoming forecasts",
            bg=self.colors["bg"],
            fg=self.colors["muted"],
            font=("Segoe UI", 10)
        )
        self.page_subtitle.pack(
            anchor="w",
            pady=(3, 0)
        )

        self.unit_button = tk.Button(
            self.header,
            text="°C",
            command=self.toggle_unit,
            bg=self.colors["card2"],
            fg=self.colors["text"],
            activebackground=self.colors["primary"],
            activeforeground="white",
            relief="flat",
            bd=0,
            font=("Segoe UI Semibold", 11),
            width=5,
            cursor="hand2"
        )
        self.unit_button.pack(
            side="right",
            padx=(10, 0)
        )

        self.refresh_button = tk.Button(
            self.header,
            text="↻ Refresh",
            command=self.get_weather,
            bg=self.colors["primary"],
            fg="white",
            activebackground=self.colors["primary_light"],
            activeforeground="white",
            relief="flat",
            bd=0,
            font=("Segoe UI Semibold", 10),
            padx=15,
            pady=8,
            cursor="hand2"
        )
        self.refresh_button.pack(side="right")

        self.search_frame = tk.Frame(
            self.content,
            bg=self.colors["input"]
        )
        self.search_frame.pack(
            fill="x",
            padx=35,
            pady=(0, 20)
        )

        tk.Label(
            self.search_frame,
            text="⌕",
            bg=self.colors["input"],
            fg=self.colors["muted"],
            font=("Segoe UI", 20)
        ).pack(
            side="left",
            padx=(16, 6)
        )

        self.city_entry = tk.Entry(
            self.search_frame,
            bg=self.colors["input"],
            fg=self.colors["text"],
            insertbackground=self.colors["text"],
            relief="flat",
            bd=0,
            font=("Segoe UI", 12)
        )
        self.city_entry.pack(
            side="left",
            fill="x",
            expand=True,
            ipady=10
        )
        self.city_entry.insert(0, "Kisumu")

        self.city_entry.bind(
            "<Return>",
            lambda event: self.get_weather()
        )

        self.search_button = tk.Button(
            self.search_frame,
            text="Get Weather",
            command=self.get_weather,
            bg=self.colors["primary"],
            fg="white",
            activebackground=self.colors["primary_light"],
            relief="flat",
            bd=0,
            font=("Segoe UI Semibold", 10),
            padx=22,
            pady=9,
            cursor="hand2"
        )
        self.search_button.pack(
            side="right",
            padx=8,
            pady=8
        )

        self.main_area = tk.Frame(
            self.content,
            bg=self.colors["bg"]
        )
        self.main_area.pack(
            fill="both",
            expand=True,
            padx=35,
            pady=(0, 25)
        )

        self.show_dashboard()

    def clear_main(self):
        for widget in self.main_area.winfo_children():
            widget.destroy()

    def show_dashboard(self):
        self.set_active("Dashboard")
        self.page_title.config(text="Weather Dashboard")
        self.page_subtitle.config(
            text="Monitor current conditions and upcoming forecasts"
        )

        self.clear_main()

        self.build_current_card()
        self.build_metrics()
        self.build_dashboard_forecast()

    def show_weather(self):
        self.set_active("Weather")
        self.page_title.config(text="Current Weather")
        self.page_subtitle.config(
            text="Detailed information about current conditions"
        )

        self.clear_main()

        if not self.current_data:
            self.show_empty_message(
                "No weather data available",
                "Search for a city to display current weather."
            )
            return

        self.build_current_card()
        self.build_weather_details()

    def show_forecast(self):
        self.set_active("Forecast")
        self.page_title.config(text="Weather Forecast")
        self.page_subtitle.config(
            text="Upcoming weather conditions"
        )

        self.clear_main()

        if not self.forecast_data:
            self.show_empty_message(
                "No forecast available",
                "Search for a city to display the forecast."
            )
            return

        self.build_hourly_full()
        self.build_daily_full()

    def show_settings(self):
        self.set_active("Settings")
        self.page_title.config(text="Settings")
        self.page_subtitle.config(
            text="Configure your weather dashboard"
        )

        self.clear_main()

        card = tk.Frame(
            self.main_area,
            bg=self.colors["card"]
        )
        card.pack(
            fill="x",
            pady=10
        )

        tk.Label(
            card,
            text="Temperature Unit",
            bg=self.colors["card"],
            fg=self.colors["text"],
            font=("Segoe UI Semibold", 15)
        ).pack(
            anchor="w",
            padx=25,
            pady=(25, 5)
        )

        tk.Label(
            card,
            text="Choose how temperatures are displayed.",
            bg=self.colors["card"],
            fg=self.colors["muted"],
            font=("Segoe UI", 10)
        ).pack(
            anchor="w",
            padx=25
        )

        unit_frame = tk.Frame(
            card,
            bg=self.colors["card"]
        )
        unit_frame.pack(
            anchor="w",
            padx=25,
            pady=20
        )

        celsius = tk.Button(
            unit_frame,
            text="Celsius °C",
            command=lambda: self.set_unit("metric"),
            bg=self.colors["primary"] if self.unit == "metric" else self.colors["card2"],
            fg="white",
            relief="flat",
            bd=0,
            padx=25,
            pady=12,
            cursor="hand2"
        )
        celsius.pack(
            side="left",
            padx=(0, 10)
        )

        fahrenheit = tk.Button(
            unit_frame,
            text="Fahrenheit °F",
            command=lambda: self.set_unit("imperial"),
            bg=self.colors["primary"] if self.unit == "imperial" else self.colors["card2"],
            fg="white",
            relief="flat",
            bd=0,
            padx=25,
            pady=12,
            cursor="hand2"
        )
        fahrenheit.pack(side="left")

        location_card = tk.Frame(
            self.main_area,
            bg=self.colors["card"]
        )
        location_card.pack(
            fill="x",
            pady=10
        )

        tk.Label(
            location_card,
            text="Search Location",
            bg=self.colors["card"],
            fg=self.colors["text"],
            font=("Segoe UI Semibold", 15)
        ).pack(
            anchor="w",
            padx=25,
            pady=(25, 5)
        )

        tk.Label(
            location_card,
            text="Enter a city in the search field above and select Get Weather.",
            bg=self.colors["card"],
            fg=self.colors["muted"],
            font=("Segoe UI", 10)
        ).pack(
            anchor="w",
            padx=25,
            pady=(0, 25)
        )

        about = tk.Frame(
            self.main_area,
            bg=self.colors["card"]
        )
        about.pack(
            fill="x",
            pady=10
        )

        tk.Label(
            about,
            text="About",
            bg=self.colors["card"],
            fg=self.colors["text"],
            font=("Segoe UI Semibold", 15)
        ).pack(
            anchor="w",
            padx=25,
            pady=(25, 5)
        )

        tk.Label(
            about,
            text="Weatherly uses the OpenWeatherMap API to retrieve real-time weather and forecast information.",
            bg=self.colors["card"],
            fg=self.colors["muted"],
            font=("Segoe UI", 10),
            wraplength=800,
            justify="left"
        ).pack(
            anchor="w",
            padx=25,
            pady=(0, 25)
        )

    def build_current_card(self):
        card = tk.Frame(
            self.main_area,
            bg=self.colors["card"]
        )
        card.pack(
            fill="x",
            pady=(0, 15)
        )

        left = tk.Frame(
            card,
            bg=self.colors["card"]
        )
        left.pack(
            side="left",
            fill="both",
            expand=True,
            padx=30,
            pady=25
        )

        if self.current_data:
            city = self.current_data["name"]
            country = self.current_data["sys"]["country"]
            temperature = self.current_data["main"]["temp"]
            feels = self.current_data["main"]["feels_like"]
            condition = self.current_data["weather"][0]["description"].title()

            location = f"{city}, {country}"
            temp = f"{temperature:.0f}°"
            feels_text = f"Feels like {feels:.1f}{self.unit_symbol}"
        else:
            location = "Kisumu, KE"
            temp = "--°"
            condition = "Search for weather"
            feels_text = "Feels like --"

        tk.Label(
            left,
            text=location,
            bg=self.colors["card"],
            fg=self.colors["text"],
            font=("Segoe UI Semibold", 22)
        ).pack(anchor="w")

        tk.Label(
            left,
            text=datetime.now().strftime(
                "%A, %d %B %Y"
            ),
            bg=self.colors["card"],
            fg=self.colors["muted"],
            font=("Segoe UI", 10)
        ).pack(
            anchor="w",
            pady=(4, 15)
        )

        tk.Label(
            left,
            text=temp,
            bg=self.colors["card"],
            fg=self.colors["text"],
            font=("Segoe UI Semibold", 58)
        ).pack(anchor="w")

        tk.Label(
            left,
            text=condition,
            bg=self.colors["card"],
            fg=self.colors["primary_light"],
            font=("Segoe UI Semibold", 14)
        ).pack(anchor="w")

        tk.Label(
            left,
            text=feels_text,
            bg=self.colors["card"],
            fg=self.colors["muted"],
            font=("Segoe UI", 10)
        ).pack(
            anchor="w",
            pady=(5, 0)
        )

        icon_frame = tk.Frame(
            card,
            bg=self.colors["card2"],
            width=190,
            height=180
        )
        icon_frame.pack(
            side="right",
            padx=30,
            pady=25
        )
        icon_frame.pack_propagate(False)

        icon_label = tk.Label(
            icon_frame,
            text="☁",
            bg=self.colors["card2"],
            fg=self.colors["primary_light"],
            font=("Segoe UI", 70)
        )
        icon_label.pack(expand=True)

        if self.current_data:
            icon_code = self.current_data["weather"][0]["icon"]
            self.load_current_icon(
                icon_code,
                icon_label
            )

    def build_metrics(self):
        if not self.current_data:
            return

        frame = tk.Frame(
            self.main_area,
            bg=self.colors["bg"]
        )
        frame.pack(
            fill="x",
            pady=(0, 15)
        )

        data = self.current_data

        values = [
            ("Feels Like", f"{data['main']['feels_like']:.1f}{self.unit_symbol}", "🌡"),
            ("Humidity", f"{data['main']['humidity']}%", "💧"),
            ("Wind", f"{data['wind']['speed']:.1f} m/s", "♨"),
            ("Pressure", f"{data['main']['pressure']} hPa", "◉"),
            ("Visibility", f"{data.get('visibility', 0) / 1000:.1f} km", "◌")
        ]

        for title, value, icon in values:
            card = tk.Frame(
                frame,
                bg=self.colors["card"]
            )
            card.pack(
                side="left",
                fill="both",
                expand=True,
                padx=4
            )

            tk.Label(
                card,
                text=icon,
                bg=self.colors["card"],
                fg=self.colors["primary_light"],
                font=("Segoe UI", 15)
            ).pack(
                anchor="w",
                padx=14,
                pady=(12, 2)
            )

            tk.Label(
                card,
                text=title,
                bg=self.colors["card"],
                fg=self.colors["muted"],
                font=("Segoe UI", 9)
            ).pack(
                anchor="w",
                padx=14
            )

            tk.Label(
                card,
                text=value,
                bg=self.colors["card"],
                fg=self.colors["text"],
                font=("Segoe UI Semibold", 12)
            ).pack(
                anchor="w",
                padx=14,
                pady=(3, 13)
            )

    def build_dashboard_forecast(self):
        if not self.forecast_data:
            return

        container = tk.Frame(
            self.main_area,
            bg=self.colors["card"]
        )
        container.pack(
            fill="both",
            expand=True
        )

        tk.Label(
            container,
            text="Upcoming Forecast",
            bg=self.colors["card"],
            fg=self.colors["text"],
            font=("Segoe UI Semibold", 14)
        ).pack(
            anchor="w",
            padx=20,
            pady=(18, 10)
        )

        row = tk.Frame(
            container,
            bg=self.colors["card"]
        )
        row.pack(
            fill="both",
            expand=True,
            padx=15,
            pady=(0, 15)
        )

        grouped = self.group_days()

        for date_key in list(grouped.keys())[:5]:
            items = grouped[date_key]
            average = sum(
                x["main"]["temp"]
                for x in items
            ) / len(items)

            condition = Counter(
                x["weather"][0]["description"]
                for x in items
            ).most_common(1)[0][0].title()

            card = tk.Frame(
                row,
                bg=self.colors["card2"]
            )
            card.pack(
                side="left",
                fill="both",
                expand=True,
                padx=4
            )

            date = datetime.strptime(
                date_key,
                "%Y-%m-%d"
            )

            tk.Label(
                card,
                text=date.strftime("%a"),
                bg=self.colors["card2"],
                fg=self.colors["muted"],
                font=("Segoe UI Semibold", 9)
            ).pack(pady=(12, 5))

            tk.Label(
                card,
                text=f"{average:.0f}{self.unit_symbol}",
                bg=self.colors["card2"],
                fg=self.colors["text"],
                font=("Segoe UI Semibold", 16)
            ).pack()

            tk.Label(
                card,
                text=condition,
                bg=self.colors["card2"],
                fg=self.colors["muted"],
                font=("Segoe UI", 8),
                wraplength=100
            ).pack(
                pady=(4, 12)
            )

    def build_weather_details(self):
        data = self.current_data

        card = tk.Frame(
            self.main_area,
            bg=self.colors["card"]
        )
        card.pack(
            fill="both",
            expand=True
        )

        tk.Label(
            card,
            text="Weather Details",
            bg=self.colors["card"],
            fg=self.colors["text"],
            font=("Segoe UI Semibold", 17)
        ).pack(
            anchor="w",
            padx=25,
            pady=(25, 20)
        )

        details = [
            ("Temperature", f"{data['main']['temp']:.1f}{self.unit_symbol}"),
            ("Feels Like", f"{data['main']['feels_like']:.1f}{self.unit_symbol}"),
            ("Humidity", f"{data['main']['humidity']}%"),
            ("Pressure", f"{data['main']['pressure']} hPa"),
            ("Wind Speed", f"{data['wind']['speed']:.1f} m/s"),
            ("Visibility", f"{data.get('visibility', 0) / 1000:.1f} km"),
            ("Condition", data["weather"][0]["description"].title()),
            ("Country", data["sys"]["country"])
        ]

        grid = tk.Frame(
            card,
            bg=self.colors["card"]
        )
        grid.pack(
            fill="x",
            padx=25
        )

        for index, (title, value) in enumerate(details):
            box = tk.Frame(
                grid,
                bg=self.colors["card2"]
            )
            box.grid(
                row=index // 2,
                column=index % 2,
                sticky="ew",
                padx=6,
                pady=6
            )

            tk.Label(
                box,
                text=title,
                bg=self.colors["card2"],
                fg=self.colors["muted"],
                font=("Segoe UI", 10)
            ).pack(
                anchor="w",
                padx=18,
                pady=(15, 2)
            )

            tk.Label(
                box,
                text=value,
                bg=self.colors["card2"],
                fg=self.colors["text"],
                font=("Segoe UI Semibold", 14)
            ).pack(
                anchor="w",
                padx=18,
                pady=(0, 15)
            )

        grid.columnconfigure(0, weight=1)
        grid.columnconfigure(1, weight=1)

    def build_hourly_full(self):
        card = tk.Frame(
            self.main_area,
            bg=self.colors["card"]
        )
        card.pack(
            fill="x",
            pady=(0, 15)
        )

        tk.Label(
            card,
            text="Next 6 Hours",
            bg=self.colors["card"],
            fg=self.colors["text"],
            font=("Segoe UI Semibold", 16)
        ).pack(
            anchor="w",
            padx=20,
            pady=(18, 12)
        )

        row = tk.Frame(
            card,
            bg=self.colors["card"]
        )
        row.pack(
            fill="x",
            padx=15,
            pady=(0, 18)
        )

        for item in self.forecast_data["list"][:2]:
            dt = datetime.fromtimestamp(item["dt"])
            temp = item["main"]["temp"]
            condition = item["weather"][0]["description"].title()

            box = tk.Frame(
                row,
                bg=self.colors["card2"]
            )
            box.pack(
                side="left",
                fill="both",
                expand=True,
                padx=5
            )

            tk.Label(
                box,
                text=dt.strftime("%H:%M"),
                bg=self.colors["card2"],
                fg=self.colors["muted"],
                font=("Segoe UI Semibold", 10)
            ).pack(pady=(15, 5))

            tk.Label(
                box,
                text=f"{temp:.0f}{self.unit_symbol}",
                bg=self.colors["card2"],
                fg=self.colors["text"],
                font=("Segoe UI Semibold", 20)
            ).pack()

            tk.Label(
                box,
                text=condition,
                bg=self.colors["card2"],
                fg=self.colors["muted"],
                font=("Segoe UI", 9)
            ).pack(pady=(4, 15))

    def build_daily_full(self):
        card = tk.Frame(
            self.main_area,
            bg=self.colors["card"]
        )
        card.pack(
            fill="both",
            expand=True
        )

        tk.Label(
            card,
            text="5-Day Forecast",
            bg=self.colors["card"],
            fg=self.colors["text"],
            font=("Segoe UI Semibold", 16)
        ).pack(
            anchor="w",
            padx=20,
            pady=(18, 12)
        )

        grouped = self.group_days()

        for date_key in list(grouped.keys())[:5]:
            items = grouped[date_key]

            average = sum(
                x["main"]["temp"]
                for x in items
            ) / len(items)

            condition = Counter(
                x["weather"][0]["description"]
                for x in items
            ).most_common(1)[0][0].title()

            date = datetime.strptime(
                date_key,
                "%Y-%m-%d"
            )

            row = tk.Frame(
                card,
                bg=self.colors["card2"]
            )
            row.pack(
                fill="x",
                padx=20,
                pady=4
            )

            tk.Label(
                row,
                text=date.strftime("%A"),
                bg=self.colors["card2"],
                fg=self.colors["text"],
                font=("Segoe UI Semibold", 10),
                width=15,
                anchor="w"
            ).pack(
                side="left",
                padx=15,
                pady=10
            )

            tk.Label(
                row,
                text=f"{average:.1f}{self.unit_symbol}",
                bg=self.colors["card2"],
                fg=self.colors["primary_light"],
                font=("Segoe UI Semibold", 11),
                width=12
            ).pack(side="left")

            tk.Label(
                row,
                text=condition,
                bg=self.colors["card2"],
                fg=self.colors["muted"],
                font=("Segoe UI", 9)
            ).pack(
                side="left",
                padx=15
            )

    def group_days(self):
        grouped = {}

        for item in self.forecast_data["list"]:
            date_key = datetime.fromtimestamp(
                item["dt"]
            ).strftime("%Y-%m-%d")

            grouped.setdefault(
                date_key,
                []
            ).append(item)

        return grouped

    def load_current_icon(self, icon_code, label):
        try:
            url = (
                f"https://openweathermap.org/img/wn/"
                f"{icon_code}@2x.png"
            )

            response = requests.get(
                url,
                timeout=10
            )

            image = Image.open(
                io.BytesIO(response.content)
            )

            image = image.resize(
                (145, 145),
                Image.Resampling.LANCZOS
            )

            self.current_icon = ImageTk.PhotoImage(image)

            label.config(
                image=self.current_icon,
                text=""
            )

        except Exception:
            label.config(
                image="",
                text="☁"
            )

    def get_weather(self):
        api_key = os.getenv("OPENWEATHER_API_KEY")

        if not api_key:
            self.show_error(
                "OpenWeatherMap API key is not configured."
            )
            return

        city = self.city_entry.get().strip()

        if not city:
            self.show_error(
                "Please enter a city name."
            )
            return

        self.search_button.config(
            state="disabled",
            text="Loading..."
        )

        try:
            params = {
                "q": city,
                "appid": api_key,
                "units": self.unit
            }

            current_response = requests.get(
                "https://api.openweathermap.org/data/2.5/weather",
                params=params,
                timeout=10
            )

            if current_response.status_code == 401:
                raise ValueError(
                    "Invalid or inactive API key."
                )

            if current_response.status_code == 404:
                raise ValueError(
                    "City not found."
                )

            current_response.raise_for_status()

            forecast_response = requests.get(
                "https://api.openweathermap.org/data/2.5/forecast",
                params=params,
                timeout=10
            )

            if forecast_response.status_code == 401:
                raise ValueError(
                    "Invalid or inactive API key."
                )

            forecast_response.raise_for_status()

            self.current_data = current_response.json()
            self.forecast_data = forecast_response.json()

            self.show_dashboard()

        except requests.exceptions.Timeout:
            self.show_error(
                "The weather service timed out."
            )

        except requests.exceptions.ConnectionError:
            self.show_error(
                "Unable to connect to the weather service."
            )

        except ValueError as error:
            self.show_error(str(error))

        except requests.exceptions.RequestException:
            self.show_error(
                "A network error occurred."
            )

        except Exception as error:
            self.show_error(
                f"An unexpected error occurred:\n{error}"
            )

        finally:
            self.search_button.config(
                state="normal",
                text="Get Weather"
            )

    def toggle_unit(self):
        if self.unit == "metric":
            self.set_unit("imperial")
        else:
            self.set_unit("metric")

    def set_unit(self, unit):
        self.unit = unit

        if unit == "metric":
            self.unit_symbol = "°C"
            self.unit_button.config(text="°C")
        else:
            self.unit_symbol = "°F"
            self.unit_button.config(text="°F")

        if self.current_data:
            self.get_weather()
        else:
            self.show_settings()

    def show_empty_message(self, title, message):
        card = tk.Frame(
            self.main_area,
            bg=self.colors["card"]
        )
        card.pack(
            fill="both",
            expand=True
        )

        tk.Label(
            card,
            text="☁",
            bg=self.colors["card"],
            fg=self.colors["primary_light"],
            font=("Segoe UI", 50)
        ).pack(pady=(80, 15))

        tk.Label(
            card,
            text=title,
            bg=self.colors["card"],
            fg=self.colors["text"],
            font=("Segoe UI Semibold", 18)
        ).pack()

        tk.Label(
            card,
            text=message,
            bg=self.colors["card"],
            fg=self.colors["muted"],
            font=("Segoe UI", 10)
        ).pack(pady=8)

    def show_error(self, message):
        messagebox.showerror(
            "Weatherly",
            message
        )


if __name__ == "__main__":
    root = tk.Tk()
    app = WeatherApp(root)
    root.mainloop()