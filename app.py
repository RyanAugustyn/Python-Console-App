from flask import Flask, request
from flask_cors import CORS
from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow
from flask_migrate import Migrate
from flask_restful import Api, Resource
from marshmallow import post_load, fields, ValidationError
from dotenv import load_dotenv
from os import environ

load_dotenv()

# Create App instance
app = Flask(__name__)

# Add DB URI from .env
app.config['SQLALCHEMY_DATABASE_URI'] = environ.get('SQLALCHEMY_DATABASE_URI')

# Registering App w/ Services
db = SQLAlchemy(app)
ma = Marshmallow(app)
api = Api(app)
CORS(app)
Migrate(app, db)

# Models
class Tree(db.Model):
    id = db.Column(db.Integer, primary_key = True)
    name = db.Column(db.String(255))
    type = db.Column(db.String(255))

def __repr__(self):
    return f'{self.name} is type? {self.type}'

# Schemas
class TreeSchema(ma.Schema):
    id = fields.Integer(primary_key = True)
    name = fields.String()
    type = fields.Bool()
    class Meta:
        fields = ("id", "name", "type")

    @post_load
    def create_tree(self, data, **kwargs):
        return Tree(**data)

tree_schema = TreeSchema
trees_schema = TreeSchema(many=True)
# Resources
class TreeListResource(Resource):
    def get(self):
        all_trees =Tree.query.all()
        return trees_schema.dump(all_trees), 200
    
    def post(self):
        new_tree_data = request.get_json()
        try:
            new_tree = tree_schema.load(new_tree_data)
            db.session.add(new_tree)
            db.session.commit()
            return tree_schema.dump(new_tree), 201
        except ValidationError as err:
            return err.messages, 400


class TreeResource(Resource):
    def get(self, tree_id):
        tree = Tree.query.get_or_404(tree_id)
        return tree_schema.dump(tree), 200

    def put(self, tree_id):
        tree = Tree.query.get_or_404(tree_id)
        if "name" in request.json:
            tree.name = request.json["name"]
        if "type" in request.json:
            tree.type = request.json["type"]
        db.session.commit()
        return tree_schema.dump(tree), 200
    
    def delete(slef, tree_id):
        tree = Tree.query.get_or_404(tree_id)
        db.session.delete(tree)
        db.session.commit()
        return '', 204


# Routes
api.add_resource(TreeListResource, '/api/trees')
api.add_resource(TreeResource, '/api/trees/<int:tree_id>')
