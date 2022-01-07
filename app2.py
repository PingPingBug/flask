from flask import Flask, request, jsonify, make_response
from flask_restful import Api, Resource, marshal_with, fields, reqparse
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy_utils.types.choice import ChoiceType
from flask_marshmallow import Marshmallow

app = Flask(__name__)
api = Api(app)


# Google Cloud SQL (change this accordingly)
PASSWORD ="your database password"
PUBLIC_IP_ADDRESS ="public ip of database"
DBNAME ="database name"
PROJECT_ID ="gcp project id"
INSTANCE_NAME ="instance name"
 

 # configuration
app.config["SECRET_KEY"] = "yoursecretkey"
app.config["SQLALCHEMY_DATABASE_URI"] = "mysql+pymysql://root:password@localhost/emp"
#app.config["SQLALCHEMY_DATABASE_URI"]= f"mysql + mysqldb://root:{PASSWORD}@{PUBLIC_IP_ADDRESS}/{DBNAME}?unix_socket =/cloudsql/{PROJECT_ID}:{INSTANCE_NAME}"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"]= True
 
db = SQLAlchemy(app)
ma = Marshmallow(app)

class ProfileModel(db.Model):
    types= [
        (u'Active', u'Active'),
        (u'Paused', u'Paused')
    ]
    __tablename__ = "profile"

    id = db.Column(db.Integer, primary_key = True, nullable = False, autoincrement=True)
    name = db.Column(db.String(50), nullable = False)
    birthdate = db.Column(db.Date, nullable = False)
    status = db.Column(ChoiceType(types), server_default="Active")


    def __repr__(self):
        return self.name

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
    def get(self):
        profile_schema = ProfileSchema()
        alll = ProfileModel.query.all()
        response = []

        for profile in alll:
            response.append(profile_schema.dump(profile))

        return make_response(jsonify(response), 200)

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

    def get(self, id):
        profile_schema = ProfileSchema()
        profile = ProfileModel.query.get(id)
        return profile_schema.dump(profile), 200

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

    def delete(self, id):
        profile = ProfileModel.query.get(id)
        db.session.delete(profile)
        db.session.commit()
        return {"message": "profile deleted succesfully"}, 204

api.add_resource(Profile, '/profiles')
api.add_resource(Edit, '/profiles/<int:id>')

if __name__ == "__main__":
    app.run(debug=True)