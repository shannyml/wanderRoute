"""Server for travel itinerary webapp."""

import json
from flask import (Flask, render_template, request, flash, session, redirect)

from model import connect_to_db, db, User, Location, Itinerary, ItineraryLocation
import os
import requests
from urllib.parse import urlencode
import crud
import werkzeug.security

app = Flask(__name__)
app.secret_key = 'SECRET'

API_KEY = os.environ['GOOGLEMAPS_KEY']
WEATHER_KEY = os.environ['WEATHER_KEY']

@app.route('/')
def homepage():

    return render_template("homepage.html")

@app.route('/create_user', methods = ['GET', 'POST'])
def register_user():
    if request.method == 'POST':

        fname = request.form.get("fname")
        lname = request.form.get('lname')
        email = request.form.get("email")
        password = request.form.get("password")
        print(password)
        hash = werkzeug.security.generate_password_hash(password)

        user = crud.get_user_by_email(email)

        if user:
            flash("Existing account with email. Login with email instead!")
            return redirect('/login')
        else:
            user = crud.create_user(fname, lname, email, hash)
            db.session.add(user)
            db.session.commit()
            session['user_id'] = user.user_id
            return redirect(f'/profile/{user.user_id}')

    return render_template('login.html')


@app.route('/login', methods =["GET", "POST"])
def login():
    if request.method == 'POST':

        email = request.form.get("login-email")
        password = request.form.get("login-password")
        
        user = crud.get_user_by_email(email)

        if werkzeug.security.check_password_hash(user.password, password):
            session['user_id'] = user.user_id
            return redirect(f'/profile/{user.user_id}')
        else:
            flash("Incorrect email or password. Try again.")
            

    return render_template("login.html")

@app.route('/profile/<user_id>')
def profile_page(user_id):

    user = crud.get_user_by_id(user_id)
    fname = user.fname
    
    itineraries = crud.get_itineraries_by_user_id(user_id)
    for itinerary in itineraries:
        for location in itinerary.locations:
            location_name = location.location_name

    return render_template('profile.html', fname = fname, itineraries = itineraries)

@app.route('/new-itinerary', methods = ['POST'])
def new_itinerary():

    itinerary_name = request.form.get("itinerary-name")
    start_date = request.form.get("trip-start")
    end_date = request.form.get("trip-end")
    user_id = session['user_id']

    new_itinerary = crud.create_itinerary(itinerary_name, user_id, start_date, end_date)
    db.session.add(new_itinerary)
    db.session.commit()
    itinerary_id = new_itinerary.itinerary_id

    return render_template('recommendations.html', itinerary_name = itinerary_name, itinerary_id=itinerary_id, user_id=user_id, API_KEY=API_KEY)


@app.route('/get-recommendations/', methods = ['GET', 'POST'])
def get_coordinates(data_type = "json"):

    location = request.args.get('interested-destination')
    print(location)

    endpoint = f"https://maps.googleapis.com/maps/api/geocode/{data_type}"
    params = {"address": location, "key": API_KEY}
    url_params = urlencode(params)
    url_1 = f"{endpoint}?{url_params}"

    response = requests.get(url_1)

    lat = (response.json()['results'][0]['geometry']['location']['lat'])
    lng = (response.json()['results'][0]['geometry']['location']['lng'])
    coordinates = {'lat': lat, 'lng': lng}

    location_type_list = location.split('=')
    location_type = location_type_list[1]
    print(location_type)

    url_2a = f"https://maps.googleapis.com/maps/api/place/nearbysearch/json?location={lat},{lng}&key={API_KEY}&radius=2000&type={location_type}"
    
    payload={}
    headers = {
    'Accept': 'application/json'
    }

    response = requests.request("GET", url_2a, headers=headers, data=payload)
    data = response.json()


    output = {'data': data, 'coordinates': coordinates}
    return output

@app.route('/get-itinerary-info', methods = ['GET', 'POST'])
def get_itinerary_info():

        user_id = session['user_id']
        info = request.json 
        info_itineraryItems = info["itineraryItems"]
        db_place_ids = crud.get_all_location_ids()
        for item in info_itineraryItems:
            place_id = item['place_id']
            location_name = item['location_name']
            lat = item['lat']
            lng = item['lng']

            if place_id not in db_place_ids:
                new_location = Location(place_id=place_id, location_name=location_name, lat=lat, lng=lng)
                print(new_location)
                db.session.add(new_location)
                db.session.commit()

        itinerary_id = info["itineraryId"]
        for item in info_itineraryItems:
            place_id = item['place_id']
            user_location = crud.create_itinerary_location(itinerary_id, place_id)
            print(user_location)
            db.session.add(user_location)
            db.session.commit()
            print(user_location)
        print("Seen C")
        return {"status": "success"}

@app.route("/get-weather")
def get_weather():

    weather_location = request.args.get("user-destination")
    
    weather_url = f"https://weather.visualcrossing.com/VisualCrossingWebServices/rest/services/weatherdata/forecast?locations={weather_location}&aggregateHours=24&unitGroup=us&shortColumnNames=false&contentType=json&key={WEATHER_KEY}"
    
    print(weather_url)

    response = requests.get(weather_url)
    data = response.json()

    return data

# @app.route("/edit-itinerary", methods = ["POST"])
# def update_itinerary():

#     new_id = request.form["itinerary-id"]
#     print(new_id)

#     return redirect("/recommendations")

@app.route("/share-itinerary", methods = ["POST"])
def share_itinerary():

    new_id = request.form["itinerary-id"]
    print(new_id)

    return redirect("/explore")

# @app.route("/logout")
# def logout():
#     session.pop('email', None)

#     return redirect('/')

@app.route("/create-itinerary")
def create_itinerary():

    return render_template('create-itinerary.html')

@app.route("/recommendations")
def show_recommendations():

    return render_template("recommendations.html")

@app.route("/weather")
def show_weather():

    return render_template("weather.html")

@app.route("/explore")
def show_explore():

    return render_template("explore.html")


if __name__ == "__main__":
    connect_to_db(app)
    app.run()