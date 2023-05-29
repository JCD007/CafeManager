import json

from flask import (
    Flask,
    render_template,
    redirect,
    flash,
    url_for,
    session,
    request,
    jsonify
)
from datetime import timedelta
from sqlalchemy.exc import (
    IntegrityError,
    DataError,
    DatabaseError,
    InterfaceError,
    InvalidRequestError,
    
)
from werkzeug.routing import BuildError
from flask_bcrypt import Bcrypt,generate_password_hash, check_password_hash
from flask_login import (
    UserMixin,
    login_user,
    LoginManager,
    current_user,
    logout_user,
    login_required,

)

from server import create_server,db,login_manager,bcrypt
from models import User, Product, ProductSchema

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

server = create_server()

@server.before_request
def session_handler():
    session.permanent = True
    server.permanent_session_lifetime = timedelta(minutes=1)


@server.route('/api/v1/auth', methods=("GET", "POST"), strict_slashes=False)
def auth():
    try:
        _json = request.get_json(force=True)   
        _dict = {'username':_json['username'], 'password':_json['password']}
        user = User().query.filter_by(username=_dict['username']).first()

        if user and check_password_hash(user.password, _dict['password']):  
            login_user(user, remember=True)
            return jsonify({'username': user.username, 'fullname': user.fullname, 'level': user.level}), 200
        else:
            return jsonify({'message': 'Invalid credentials!'}), 401
    except Exception as e:
        return jsonify({'message': 'Internal server error!'}) ,500


@server.route('/api/v1/register', methods=['POST'])
def create_user():
    _json = request.get_json(force=True) 
    _dict = {'username':_json['username'], 'password':_json['password']}

    user = User().query.filter_by(username=_dict['username']).first()
    if user:
        return jsonify({'message': 'Username already exists!'}), 409
    else:
        user = User(
		username=_dict['username'], 
		fullname=_dict['username'], 
		password=bcrypt.generate_password_hash(_dict['password']), 
		level=1)		
        db.session.add(user)
        res = db.session.commit()
        print(res)
        return jsonify({'message': 'User created successfully!'}), 201

@server.route("/logout")
@login_required
def logout():
    logout_user()
    return redirect(url_for('login'))

@server.route("/api/v1/products",  methods=["GET"], strict_slashes=False)
@login_required
def products():
    data = Product().query.all()
    schema = ProductSchema(many=True)  
    print(schema.dump(data))
    return jsonify(schema.dump(data)), 200 


if __name__ == "__main__":
    server.run(ssl_context='adhoc', debug=True)