# Simple map and weather app 

from string import Template 
import pyowm
owm = pyowm.OWM('YOURAPIKEY')  
from flask import Flask,render_template,request
from geopy.geocoders import Bing
geolocator= Bing("YOURAPIKEY", format_string=None, scheme=None, user_agent=None)

app = Flask(__name__)

@app.route("/<city>")
def create_homepage(city):
    loca = geolocator.geocode(city) # geocodeing: address to coordinates
    latlong=str(loca.latitude)+","+str(loca.longitude)
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
    return create_homepage(text)
	
if __name__ == '__main__':
    app.run(use_reloader=True,debug=True)
