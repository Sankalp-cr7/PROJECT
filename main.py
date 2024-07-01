from kivy.app import App
from kivy.uix.label import Label
from kivy.uix.boxlayout import BoxLayout
from kivy.clock import Clock
import requests
import time
from plyer import notification
import sys, subprocess

api_key = '2a5da68326a774a1a5c4a6b84fbe2ada'
user_input = "West Delhi"

class Sustainable_Future(App):

    def build(self):
        layout = BoxLayout(orientation='vertical')
        self.weather_label = Label(text='', font_size=24, halign='center',bold=True,underline=True)
        layout.add_widget(self.weather_label)
        self.check_weather()  # Start checking weather on app start
        return layout

    def clear_screen(self):
        operating_system = sys.platform
        if operating_system == 'win32':
            subprocess.run('cls', shell=True)
        elif operating_system == 'linux' or operating_system == 'darwin':
            subprocess.run('clear', shell=True)

    def notify(self, title, message, icon):
        notification.notify(title=title, message=message, app_icon=icon, timeout=10)

    def check_weather(self, *args):
        weather_data = requests.get(
            f"https://api.openweathermap.org/data/2.5/weather?q={user_input}&units=imperial&APPID={api_key}")

        if weather_data.json()['cod'] == "404":
            self.weather_label.text = "No city found !"
            return

        weather = weather_data.json()['weather'][0]['main']
        temp = round(weather_data.json()['main']['temp'])

        self.weather_label.text = f"The weather in {user_input} is {weather}\n"
        self.weather_label.text += f"The temperature in {user_input} is {temp} °F"

        if weather == "Rain":
            self.notify("ALERT", "Watering is not important today. As, it's raining.", "eco-light.ico")
            time.sleep(2)
            self.clear_screen()

        timestamp = time.strftime('%H')

        if int(timestamp) > 12 and weather != "Rain":
            self.notify("ALERT", "Water plants now!", "watering-plants.ico")
            time.sleep(2)
            self.clear_screen()

        elif int(temp) > 87:
            self.notify("ALERT", "Watering plants is important.", "eco-light.ico")
            time.sleep(2)
            self.clear_screen()

        # Schedule the next weather check after 5 minutes (300 seconds)
        Clock.schedule_once(self.check_weather, 300)

if __name__ == '__main__':
    Sustainable_Future().run()
