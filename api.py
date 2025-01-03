from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_restful import Resource, Api, reqparse, fields, marshal_with, abort

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.db'
db = SQLAlchemy(app)
api = Api(app)

class UserModel(db.Model):
    id = db.Column(db.Integer, primary_key = True)
    name = db.Column(db.String(80), unique = True, nullable = False)

    def __repr__(self):
        return f'ID {self.id } Name {self.name}'
    
user_args = reqparse.RequestParser()
user_args.add_argument('name', type=str, required=True, help='Name cannot be blank')

#Serializer
userFields = {
    'id':fields.Integer,
    'name':fields.String
}

class Users(Resource):
    @marshal_with(userFields)
    def get(self):
        users = UserModel.query.all()
        return users
    
    @marshal_with(userFields)
    def post(self):
        args = user_args.parse_args()
        user = UserModel(name=args['name'])
        db.session.add(user)
        db.session.commit()
        user = UserModel.query.all()
        return user, 201

api.add_resource(Users, '/api/users/')


@app.route('/')
def home():
    return '<h1>Flask Rest Api</h1>'

if __name__ == '__main__':
    app.run(debug=True)

    