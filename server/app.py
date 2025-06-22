from flask import Flask, jsonify, request
from flask_migrate import Migrate
from flask_restful import Api, Resource
from models import db, Plant

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///plants.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.json.compact = True

db.init_app(app)
migrate = Migrate(app, db)

api = Api(app)

# ---------- ROUTES ----------

class Plants(Resource):
    def get(self):
        plants = Plant.query.all()
        return [plant.to_dict() for plant in plants], 200

    def post(self):
        data = request.get_json()
        try:
            new_plant = Plant(
                name=data["name"],
                image=data["image"],
                price=data["price"]
            )
            db.session.add(new_plant)
            db.session.commit()
            return new_plant.to_dict(), 201
        except Exception as e:
            return {"error": str(e)}, 400


class PlantByID(Resource):
    def get(self, id):
        plant = Plant.query.get(id)
        if plant:
            return plant.to_dict(), 200
        return {"error": "Plant not found"}, 404


# ---------- REGISTER ROUTES ----------

api.add_resource(Plants, "/plants")
api.add_resource(PlantByID, "/plants/<int:id>")


# ---------- RUN APP ----------

if __name__ == '__main__':
    app.run(port=5555, debug=True)
