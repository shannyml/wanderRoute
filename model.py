"""Models for travel log app."""

from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class User(db.Model):

    __tablename__ = "users"

    user_id = db.Column(db.Integer, autoincrement = True, primary_key = True)
    fname = db.Column(db.String, nullable = False)
    lname = db.Column(db.String, nullable = False)
    email = db.Column(db.String, unique = True, nullable = False)
    password = db.Column(db.String, nullable = False)

 
    def __repr__(self):
        return f'<User user_id={self.user_id}, first name={self.fname} email={self.email} >'

class Itinerary(db.Model):

    __tablename__ = "itineraries"

    itinerary_id = db.Column(db.Integer, autoincrement = True, primary_key = True)
    itinerary_name = db.Column(db.String, nullable = False)
    user_id = db.Column(db.Integer, db.ForeignKey(User.user_id), nullable = False)
    start_date = db.Column(db.String, nullable = True)
    end_date = db.Column(db.String, nullable = True)

    user = db.relationship("User", backref = "itineraries")
    locations = db.relationship("Location", secondary = "itineraries_locations", back_populates = "itineraries")

    def __repr__(self):
        return f'<Itinerary itinerary_id={self.itinerary_id}, itinerary_name={self.itinerary_name}, user_id= {self.user_id} >'

class Location(db.Model):

    __tablename__ = "locations"

    place_id = db.Column(db.String, primary_key = True)
    location_name = db.Column(db.String, nullable = True)
    lat = db.Column(db.Float, nullable = False)
    lng = db.Column(db.Float, nullable = False)

    itineraries = db.relationship("Itinerary", secondary = "itineraries_locations", back_populates = "locations")

    def __repr__(self):
        return f'<Location place_id={self.place_id}, location name={self.location_name} >'

class ItineraryLocation(db.Model):

    __tablename__ = "itineraries_locations"

    itinerary_place_id = db.Column(db.Integer, autoincrement = True, primary_key = True)
    itinerary_id = db.Column(db.Integer, db.ForeignKey("itineraries.itinerary_id"), nullable = False)
    place_id = db.Column(db.String, db.ForeignKey("locations.place_id"), nullable = False)


    def __repr__(self):
        return f'<Itinerary IL_id={self.itinerary_place_id}, Location: itinerary_id={self.itinerary_id}, place_id={self.place_id} >'


def connect_to_db(flask_app, db_uri="postgresql:///travel", echo=False):
    flask_app.config["SQLALCHEMY_DATABASE_URI"] = db_uri
    flask_app.config["SQLALCHEMY_ECHO"] = echo
    flask_app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

    db.app = flask_app
    db.init_app(flask_app)

    print("Connected to the db!")

if __name__ == "__main__":
    from server import app

    # Call connect_to_db(app, echo=False) if your program output gets
    # too annoying; this will tell SQLAlchemy not to print out every
    # query it executes.

    connect_to_db(app, echo=False)