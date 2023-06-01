#!/usr/bin/env python3

import os

BASE_DIR = os.path.abspath(os.path.dirname(__file__))
DATABASE = os.environ.get(
    "DB_URI", f"sqlite:///{os.path.join(BASE_DIR, 'instance/app.db')}"
)

from flask import Flask, make_response, jsonify, request
from flask_migrate import Migrate
from flask_restful import Api, Resource
import ipdb

from models import db, Activity, Camper, Signup

app = Flask(__name__)
api = Api(app)

app.config["SQLALCHEMY_DATABASE_URI"] = DATABASE
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
app.json.compact = False

migrate = Migrate(app, db)

db.init_app(app)


class Home(Resource):
    def get(self):
        return {"camping_world": "welcome"}


api.add_resource(Home, "/")


class Campers(Resource):
    def get(self):
        response = make_response(
            jsonify([camper.to_dict() for camper in Camper.query.all()]), 200
        )

        return response

    def post(self):
        try:
            new_camper = Camper(name=request.json["name"], age=request.json["age"])
            db.session.add(new_camper)
            db.session.commit()
        except Exception as e:
            return make_response(jsonify({"error": str(e)}), 400)

        response = make_response(jsonify(new_camper.to_dict()), 201)

        return response


api.add_resource(Campers, "/campers")


class CamperByID(Resource):
    def get(self, id):
        camper = db.session.get(Camper, id)
        if not camper:
            response = make_response(jsonify({"error": "404: Camper not found"}), 404)
            return response
        camper_dict = camper.to_dict()
        camper_dict["activities"] = [
            activity.to_dict() for activity in camper.activities
        ]
        response = make_response(jsonify(camper_dict), 200)

        return response


api.add_resource(CamperByID, "/campers/<int:id>")


class Activities(Resource):
    def get(self):
        return make_response(
            jsonify([activity.to_dict() for activity in Activity.query.all()]), 200
        )


api.add_resource(Activities, "/activities")


class ActivityByID(Resource):
    def delete(self, id):
        activity = db.session.get(Activity, id)
        if activity:
            for signup in activity.signups:
                db.session.delete(signup)
                db.session.commit()
            db.session.delete(activity)
            db.session.commit()

            return make_response(jsonify({}), 204)
        else:
            return make_response(jsonify({"error": "404: Activity not found"}), 404)


api.add_resource(ActivityByID, "/activities/<int:id>")


class Signups(Resource):
    def post(self):
        try:
            new_signup = Signup(
                time=request.json["time"],
                camper_id=request.json["camper_id"],
                activity_id=request.json["activity_id"],
            )
            db.session.add(new_signup)
            db.session.commit()
        except Exception as e:
            return make_response(jsonify({"error": str(e)}), 400)

        return make_response(jsonify(new_signup.to_dict()), 201)


api.add_resource(Signups, "/signups")


if __name__ == "__main__":
    app.run(port=5555, debug=True)
