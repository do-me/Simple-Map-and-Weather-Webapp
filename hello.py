# Simple map and weather app 

from string import Template # hier template in anderes file auslagern
import pyowm
from flask import Flask,render_template,request
from geopy.geocoders import Bing
geolocator= Bing("AhcCdXdVNe28OX3wIvvEFidep2NCH63T7tV16_httIbFgiZ8CSPfexqlvUqGcM6Y",
                 format_string=None, scheme=None, user_agent=None)

app = Flask(__name__)

@app.route("/<city>")
def whatever_homepage(city):
    loca = geolocator.geocode(city) # geocodeing: address to coordinates
    latlong=str(loca.latitude)+","+str(loca.longitude)
    
    owm = pyowm.OWM('2e5c854765a64f8eb6f3ab04bebdc24c')  # You MUST provide a valid API key
    observation = owm.weather_around_coords(loca.latitude, loca.longitude) 
    w = observation[0].get_weather()
    
    weather=str(round(w.get_temperature('celsius')["temp"])) + " °C, " + str(w.get_detailed_status()) 
    
    return Template(render_template('standard.html')).substitute(latlong=latlong, title=city.capitalize(), weather=weather)

@app.route("/")
def places():
    return render_template('my-form.html')

@app.route('/', methods=['POST'])
def my_form_post():
    text = request.form['text']
    return whatever_homepage(text)


#@app.route("/Berlin") # case sensitive!
#def berlin():
    
#    return """<html><h1>Aha! Du suchst Berlin?</h1>
#<iframe src="https://player.vimeo.com/video/105955605" width="500" height="281" frameborder="0" webkitallowfullscreen mozallowfullscreen allowfullscreen></iframe>"""


if __name__ == '__main__':
    app.run(use_reloader=True,debug=True)
