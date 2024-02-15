from tkinter import *
from tkinter import messagebox
from configparser import ConfigParser
import requests
from datetime import datetime, timedelta

url = 'https://api.openweathermap.org/data/2.5/weather?q={}&appid={}'

config_file = 'config.ini'
config = ConfigParser()
config.read(config_file)
api_key = config['api_key']['key']


def get_weather(city):
    result = requests.get(url.format(city, api_key))
    if result:
        json = result.json()
        # (City, Country, temp_celsius, icon, weather)
        city = json['name']
        country = json['sys']['country']
        temp_kelvin = json['main']['temp']
        temp_celsius = temp_kelvin - 273.15
        icon = json['weather'][0]['icon']
        weather = json['weather'][0]['main']
        final = (city, country, temp_celsius, icon, weather)
        return final
    else:
        return None



def get_weather_forecast(city):
    result = requests.get(f'https://api.openweathermap.org/data/2.5/forecast?q={city}&appid={api_key}')
    if result:
        json = result.json()
        forecast_data = json['list']
        forecast = []
        today = datetime.today().date()
        for i, data in enumerate(forecast_data):
            date = today + timedelta(days=i)
            if len(forecast) == 3:
                break
            if date != today and date.day != today.day:  # Пропускаем текущий день и повторяющиеся даты
                date_str = date.strftime('%d.%m.%y')
                weather = data['weather'][0]['main']
                temp_kelvin = data['main']['temp']
                temp_celsius = temp_kelvin - 273.15
                forecast.append((date_str, weather, f'{temp_celsius:.2f}°C'))
        return forecast
    else:
        return None


def search():
    city = city_text.get()
    weather = get_weather(city)
    forecast = get_weather_forecast(city)
    if weather and forecast:
        location_lbl['text'] = f'{weather[0]}, {weather[1]}'
        temp_lbl['text'] = f'{weather[2]:.2f}°C'
        weather_lbl['text'] = weather[4]
        img["file"] = f'weather_icons/{weather[3]}.png'
        for widget in forecast_frame.winfo_children():
            widget.destroy()  # Удаляем предыдущий прогноз перед добавлением нового
        for i, (date, weather_type, temp) in enumerate(forecast):
            square_frame = Frame(forecast_frame, bg='#f0f0f0', bd=1, relief='solid', highlightbackground='#f0f0f0', highlightthickness=1, padx=5, pady=5)
            square_frame.pack(side=LEFT, padx=10)
            date_label = Label(square_frame, text=date, font=('Arial', 14, 'bold'), bg='#f0f0f0')
            date_label.pack(side=TOP, padx=5)
            weather_label = Label(square_frame, text=f'{weather_type}\n{temp}', font=('Arial', 14, 'bold'), bg='#f0f0f0')
            weather_label.pack(side=BOTTOM, padx=5)
    else:
        messagebox.showerror('Ошибка', f'Город не найден: {city}')


app = Tk()
app.title("Weather App")
app.geometry('500x600')
app.configure(bg='#f0f0f0')

search_icon = PhotoImage(file="D:/pythonProject/WeatherApp/weather_icons/search_icon.png")

city_text = Entry(app, width=30, font=('Arial', 14, 'bold'), bd=2, relief="solid")
city_text.pack(pady=20)

search_btn = Button(app, image=search_icon, borderwidth=0, command=search, bg='#f0f0f0', highlightthickness=0)
search_btn.pack()

location_lbl = Label(app, text='', font=('Arial', 20, 'bold'), bg='#f0f0f0')
location_lbl.pack(pady=10)

img = PhotoImage(file="")
image = Label(app, image=img)
image.pack()

temp_lbl = Label(app, text='', font=('Arial', 17, 'bold'), bg='#f0f0f0')
temp_lbl.pack()

weather_lbl = Label(app, text='', font=('Arial', 15, 'bold'), bg='#f0f0f0')
weather_lbl.pack()

forecast_frame = Frame(app, bg='#f0f0f0')
forecast_frame.pack(pady=10)

app.mainloop()