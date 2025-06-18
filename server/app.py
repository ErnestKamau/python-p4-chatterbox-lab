from flask import Flask, request, make_response, jsonify
from flask_cors import CORS
from flask_migrate import Migrate

from models import db, Message

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///app.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.json.compact = False

CORS(app)
migrate = Migrate(app, db)

db.init_app(app)

@app.route('/')
def index():
    return make_response(jsonify({"Message": "Welcome to the Chatterbox API"}))


@app.route('/messages', methods=['GET'])
def messages():
    all_messages = [m.to_dict() for m in Message.query.order_by(Message.created_at).all()]
    return jsonify(all_messages), 200



@app.route('/messages/<int:id>', methods=['PATCH', 'DELETE'])
def messages_by_id(id):
    message = Message.query.filter(Message.id == id).first()
    
    if message == None:
        return make_response(jsonify({"message": "This message does not exist in our database. Please try again."}), 404)
    
    else:
        if request.method == 'PATCH':
            data = request.get_json()
            
            if not data or 'body' not in data:
                return jsonify({'error': 'body is required'}), 400
            
            message.body = data['body']
            
            db.session.commit()
            
            return jsonify(message.to_dict()), 200
        
        
        elif request.method == 'DELETE':
            db.session.delete(message)
            db.session.commit()
            
            return make_response(jsonify({"message": "Message deleted."}), 200)
        
        
@app.route('/messages', methods=['POST'])
def create_message():
    data = request.get_json()
    
    if not data or 'body' not in data or 'username' not in data:
        return jsonify({'error': 'body and username are required'}), 400
    
    new_message = Message(body=data['body'], username=data['username'])
    
    db.session.add(new_message)
    db.session.commit()
    
    return jsonify(new_message.to_dict()), 201




if __name__ == '__main__':
    app.run(port=5555)
