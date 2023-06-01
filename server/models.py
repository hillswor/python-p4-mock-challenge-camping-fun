from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import MetaData
from sqlalchemy.orm import validates
from sqlalchemy.ext.associationproxy import association_proxy
from sqlalchemy_serializer import SerializerMixin

convention = {
    "ix": "ix_%(column_0_label)s",
    "uq": "uq_%(table_name)s_%(column_0_name)s",
    "ck": "ck_%(table_name)s_%(constraint_name)s",
    "fk": "fk_%(table_name)s_%(column_0_name)s_%(referred_table_name)s",
    "pk": "pk_%(table_name)s",
}

metadata = MetaData(naming_convention=convention)

db = SQLAlchemy(metadata=metadata)


class Activity(db.Model, SerializerMixin):
    __tablename__ = "activities"

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String)
    difficulty = db.Column(db.Integer)

    signups = db.relationship("Signup", backref="activity")
    campers = association_proxy("signups", "camper")

    serialize_rules = ("-signups",)

    def __repr__(self):
        return f"<Activity {self.id}: {self.name}>"


class Camper(db.Model, SerializerMixin):
    __tablename__ = "campers"

    @validates("name")
    def name_validator(self, key, name):
        if not name:
            raise ValueError("400: Validation error")
        return name

    @validates("age")
    def age_validator(self, key, age):
        if age < 8 or age > 18:
            raise ValueError("400: Validation error")
        return age

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String, nullable=False)
    age = db.Column(db.Integer)

    signups = db.relationship("Signup", backref="camper")
    activities = association_proxy("signups", "activity")

    serialize_rules = ("-signups", "-activities")

    def __repr__(self):
        return f"<Camper {self.id}: {self.name}>"


class Signup(db.Model, SerializerMixin):
    __tablename__ = "signups"

    @validates("time")
    def time_validator(self, key, time):
        if time < 0 or time > 23:
            raise ValueError("400: Validation error")
        return time

    id = db.Column(db.Integer, primary_key=True)
    time = db.Column(db.Integer)
    activity_id = db.Column(db.Integer, db.ForeignKey("activities.id"))
    camper_id = db.Column(db.Integer, db.ForeignKey("campers.id"))

    serialize_rules = ("-activity", "-camper")

    def __repr__(self):
        return f"<Signup {self.id}>"
