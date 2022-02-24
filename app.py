from flask import Flask, render_template
import matplotlib
import matplotlib.pyplot as pplot
import numpy as np
import requests
from datetime import datetime

from env import WEATHER_URL_API

app = Flask(__name__)

@app.route("/")
def hello_world():
    return render_template("index.html")

@app.route("/temp paris")
def temp_paris():
    
    api_response = requests.get(WEATHER_URL_API)
    api_data = api_response.json()

    temperature = []
    temperature_date = []
    
    for date in api_data:
        if "2022" in date:
            if "13:00:00" in date:
                date_time = datetime.strptime(date, "%Y-%m-%d %H:%M:%S")
                parse_date = date_time.strftime("%a, %d \n%Hh")
                temperature_date.append(parse_date)
                parse_temp = api_data[date]["temperature"]["sol"] - 272.15  
                temperature.append(parse_temp)
            
    if temperature and temperature_date != []:
         draw_graph( (temperature, temperature_date))
         with open("static/data.svg") as data:
            output = str(data.read())
    else:
        output = "Unable to draw graph, please check console."

    return render_template("weather.html", weather=output)


def draw_graph(data:tuple) -> str:
    pplot.ylabel("°C")
    pplot.bar(data[1], data[0])
    pplot.savefig("static/data.svg")
