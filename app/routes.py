from app import app, ma, db, api
from app.models import ProfileModel
from flask_restful import Resource
from flask_restful import reqparse
from flask_restful_swagger import swagger
from flask import jsonify, make_response
from marshmallow import fields

class ProfileSchema(ma.SQLAlchemySchema):
    class Meta:
        model = ProfileModel

    id = ma.auto_field()
    name = ma.auto_field()
    birthdate = ma.auto_field()
    status = ma.auto_field()


parser = reqparse.RequestParser()
parser.add_argument('name')
parser.add_argument('birthdate')
parser.add_argument('status')

update = reqparse.RequestParser() 
update.add_argument('name')
update.add_argument('birthdate')
update.add_argument('status')


resolve_fields = {
    'id': fields.Integer,
    'name': fields.String,
    'birthdate': fields.DateTime,
    'status': fields.String,
}

author_schema = ProfileSchema()

class Profile(Resource):

    @swagger.operation()
    def get(self):
        profile_schema = ProfileSchema()
        alll = ProfileModel.query.all()
        response = []

        for profile in alll:
            response.append(profile_schema.dump(profile))

        return make_response(jsonify(response), 200)

    @swagger.operation()
    def post(self):
        profile_schema = ProfileSchema()
        args = parser.parse_args()
        profile = ProfileModel(name=args["name"], birthdate=args["birthdate"], status=args["status"])
        db.session.add(profile)
        db.session.commit()
        return profile_schema.dump(profile) , 201

    def delete(self):
        pass

    def put(self):
        pass

class Edit(Resource):

    @swagger.operation()
    def get(self, id):
        profile_schema = ProfileSchema()
        profile = ProfileModel.query.get(id)
        return profile_schema.dump(profile), 200

    @swagger.operation()
    def patch(self, id):
        args = update.parse_args()    
        profile_schema = ProfileSchema()
        profile = ProfileModel.query.get(id)

        if args['name']!= None:
            profile.name = args['name']

        if args['birthdate']!= None:
            profile.birthdate = args['birthdate']

        if args['status']!= None:
            profile.status = args['status']   

        db.session.commit()

        return profile_schema.dump(profile)         

    def post(self, id):
        pass

    def put(self, id):
        pass

    @swagger.operation()
    def delete(self, id):
        profile = ProfileModel.query.get(id)
        db.session.delete(profile)
        db.session.commit()
        return {"message": "profile deleted succesfully"}, 204

api.add_resource(Profile, '/profiles')
api.add_resource(Edit, '/profiles/<int:id>')
