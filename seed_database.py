"""Script to seed database."""

import os
import json
from random import choice

import crud
import model
import server
import werkzeug.security

os.system("dropdb travel")

os.system("createdb travel")

model.connect_to_db(server.app)

model.db.create_all()

# seed test user
with open('data/test_users.js') as f:
    user_data = json.loads(f.read())

user_in_db = []

for user in user_data:
    fname = user["fname"]
    lname = user["lname"]
    email = user["email"]
    password = user["password"]
    hash = werkzeug.security.generate_password_hash(password)

    db_user = crud.create_user(fname, lname, email, hash)
    user_in_db.append(db_user)

model.db.session.add_all(user_in_db)
model.db.session.commit()


# seed test itineraries
with open ('data/test_itineraries.js') as f:
    itinerary_data = json.loads(f.read())

itinerary_in_db = []

for itinerary in itinerary_data:
    itinerary_name = itinerary["itinerary_name"]
    user_id = itinerary["user_id"]
    start_date = itinerary["start_date"]
    end_date = itinerary["end_date"]

    db_itinerary = crud.create_itinerary(itinerary_name, user_id, start_date, end_date)
    itinerary_in_db.append(db_itinerary)

model.db.session.add_all(itinerary_in_db)
model.db.session.commit()


# seed test locations
with open('data/test_locations.js') as f:
    location_data = json.loads(f.read())

location_in_db = []

for location in location_data:
    place_id = location["place_id"]
    location_name = location["location_name"]
    lat = location["lat"]
    lng = location["lng"]

    db_location = crud.create_location(place_id, location_name, lat, lng)
    # adds random location to itineraries that adds it to the join table database
    db_location.itineraries.append(choice(itinerary_in_db))
    location_in_db.append(db_location)

model.db.session.add_all(location_in_db)
model.db.session.commit()

