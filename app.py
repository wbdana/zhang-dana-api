from flask import Flask, jsonify, request
from flask.ext.sqlalchemy import SQLAlchemy
from flask_cors import CORS, cross_origin
import os

app = Flask(__name__)
app.config.from_object(os.environ['APP_SETTINGS'])
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['CORS_HEADERS'] = 'Content-Type'
cors = CORS(app, resources={r"/rsvp": {"origins": "http://localhost:3000/"}})
db = SQLAlchemy(app)

from models import Rsvp

@app.route('/')
def index():
    return jsonify(status=200)

# Get all RSVPs from every guest
@app.route('/rsvps')
def all_rsvps():
    query_result = Rsvp.query.all()
    return jsonify(result=[item.serialize for item in query_result])

@app.route('/rsvp', methods=['POST'])
@cross_origin(origin='https://zhang-dana.herokuapp.com', headers=['Content-Type'])
def add_rsvp():
    rsvp_obj = request.get_json()
    if rsvp_obj['name'] == "":
        return 'Name cannot be blank!', 400
    if rsvp_obj['email'] == "":
        return 'Email cannot be blank!', 400
    if rsvp_obj['rehearsal'] == "True":
        rsvp_obj['rehearsal'] = True
    else:
        rsvp_obj['rehearsal'] = False
    if rsvp_obj['wedding'] == "True":
        rsvp_obj['wedding'] = True
    else:
        rsvp_obj['wedding'] = False
    if rsvp_obj['brunch'] == "True":
        rsvp_obj['brunch'] = True
    else:
        rsvp_obj['brunch'] = False
    new_rsvp = Rsvp(rsvp_obj['name'], rsvp_obj['email'], rsvp_obj['rehearsal'], rsvp_obj['wedding'], rsvp_obj['brunch'])
    db.session.add(new_rsvp)
    db.session.commit()
    return 'We can\'t wait to see you!', 200


if __name__ == '__main__':
    app.run()
