#!/usr/bin/env python3

from flask import Flask, jsonify, request, make_response
from flask_migrate import Migrate
from flask_restful import Api, Resource

from models import db, Plant

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///plants.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.json.compact = True

migrate = Migrate(app, db)
db.init_app(app)

api = Api(app)

class Plants(Resource):
    def get(self):
        plants = Plant.query.all()
        plant_list = [{
            'id': plant.id,
            'name': plant.name,
            'image': plant.image,
            'price': float(plant.price)
        } for plant in plants]
        return jsonify(plant_list)

    def post(self):
        data = request.get_json()
        if not data:
            return make_response(jsonify({'error': 'Invalid JSON data'}), 400)

        new_plant = Plant(
            name=data['name'],
            image=data['image'],
            price=data['price']
        )

        db.session.add(new_plant)
        db.session.commit()

        return jsonify({
            'id': new_plant.id,
            'name': new_plant.name,
            'image': new_plant.image,
            'price': float(new_plant.price)
        }), 201

class PlantByID(Resource):
    def get(self, id):
        plant = Plant.query.get(id)
        if not plant:
            return make_response(jsonify({'error': 'Plant not found'}), 404)
        return jsonify({
            'id': plant.id,
            'name': plant.name,
            'image': plant.image,
            'price': float(plant.price)
        })

api.add_resource(Plants, '/plants')
api.add_resource(PlantByID, '/plants/<int:id>')
        

if __name__ == '__main__':
    app.run(port=5555, debug=True)
