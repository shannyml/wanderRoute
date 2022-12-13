"""CRUD operations."""

from model import db, User, Itinerary, Location, ItineraryLocation

def create_user(fname, lname, email, password):
    """Create and return a new user."""

    user = User(fname = fname, lname =lname, email = email, password = password)

    return user

def create_itinerary(itinerary_name, user_id, start_date, end_date):

    itinerary = Itinerary(itinerary_name = itinerary_name, user_id = user_id, start_date = start_date, end_date = end_date)

    return itinerary

def create_location(place_id, location_name, lat, lng):

    location = Location(place_id= place_id, location_name = location_name, lat = lat, lng = lng)

    return location

def create_itinerary_location(itinerary_id, place_id):

    itinerary_location = ItineraryLocation(itinerary_id=itinerary_id, place_id=place_id)

    return itinerary_location

def get_user_by_email(email):

    return User.query.filter(User.email == email).first()

def get_user_by_password(password):

    return User.query.filter(User.password == password).first()

def get_user_by_id(user_id):

    return User.query.filter(User.user_id == user_id).first()

def get_itineraries_by_user_id(user_id):

    return Itinerary.query.filter(Itinerary.user_id == user_id).options(db.joinedload('locations')).all()

def get_location_by_location_name(location_name):

    return Location.query.filter(Location.location_name == location_name).first()

def get_itinerary_by_user_id_itinerary_name(user_id, itinerary_name):
    
    return Itinerary.query.filter(Itinerary.user_id == user_id, Itinerary.itinerary_name == itinerary_name).first()

# def get_itinerary_id_by_itinerary_name_user_id(itinerary_name, user_id):

#     return Itinerary.query.filter(Itinerary.itinerary_name == itinerary_name and User.user_id == user_id).first()

def get_all_location_ids():

    locations_id = []
    locations = Location.query.all()
    for location in locations:
        id = location.place_id
        locations_id.append(id)

    return locations_id

def get_all_locations():

    return Location.query.all()


if __name__ == "__main__":
    from server import app
    from model import connect_to_db
    connect_to_db(app)