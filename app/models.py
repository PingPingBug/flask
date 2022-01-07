from app import db
from sqlalchemy_utils.types.choice import ChoiceType

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