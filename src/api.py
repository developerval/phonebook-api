from flask import Flask, request, jsonify, make_response
from flask_sqlalchemy import SQLAlchemy
import uuid
from werkzeug.security import generate_password_hash, check_password_hash

app = Flask(__name__)

app.config['SECRET_KEY'] = 'secretkey'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:////Users/valentine/Desktop/hackajob/phonebook-api/src/phonebook.db'

db = SQLAlchemy(app)


class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    public_id = db.Column(db.String(20), unique=True)
    name = db.Column(db.String(50))
    password = db.Column(db.String(80))
    admin = db.Column(db.Boolean)


class Entry(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    first_name = db.Column(db.String(60))
    last_name = db.Column(db.String(60))
    phone_number = db.Column(db.String(25))


@app.route('/user', methods=['POST'])
def create_user():
    data = request.get_json()
    hashed_pass = generate_password_hash(data['password'], method='sha256')

    new_user = User(public_id=str(uuid.uuid4()),
                    name=data['name'], password=hashed_pass, admin=False)
    db.session.add(new_user)
    db.session.commit()

    return jsonify({'message': 'New User added'})


@app.route('/user/<user_id>', methods=['PUT'])
def update_user():
    return ''


@app.route('/user/<full_name>', methods=['DELETE'])
def delete_entry_by_name():
    return ''


@app.route('/entries/<id>', methods=['DELETE'])
def delete_entry_by_id(id):

    entry = Entry.query.filter_by(id=id).first()

    if not entry:
        return jsonify({'Message': 'ID not found'})

    entry_data = {}
    entry_data['first_name'] = entry.first_name
    entry_data['last_name'] = entry.last_name
    entry_data['phone_number'] = entry.phone_number

    return jsonify({'Entry': entry_data})


@app.route('/entries', methods=['GET'])
def get_all_entries():
    entries = Entry.query.all()
    out = []

    for entry in entries:
        entry_data = {}
        entry_data['first_name'] = entry.first_name
        entry_data['last_name'] = entry.last_name
        entry_data['phone_number'] = entry.phone_number
        out.append(entry_data)

    return jsonify({'Entries': out})


@app.route('/entries/<id>', methods=['GET'])
def get_entry_by_id(id):

    entry = Entry.query.filter_by(id=id).first()

    if not entry:
        return jsonify({'Message': 'ID not found'})

    entry_data = {}
    entry_data['first_name'] = entry.first_name
    entry_data['last_name'] = entry.last_name
    entry_data['phone_number'] = entry.phone_number

    return jsonify({'Entry': entry_data})


@app.route('/entries', methods=['POST'])
def create_entry():
    data = request.get_json()
    if db.session.query(Entry).filter(Entry.phone_number == data['phone_number']).count() == 0:
        new_entry = Entry(
            first_name=data['first_name'], last_name=data['last_name'],
            phone_number=data['phone_number'].replace(" ", ""))

        db.session.add(new_entry)
        db.session.commit()
        return jsonify({'Message': "New Entry added"})
    else:
        return make_response(jsonify({'Error': 'Phone number already exists'}), 400)


if __name__ == '__main__':
    app.run(debug=True)
