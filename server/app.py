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

@app.route('/messages',methods=['GET'])
def messages():
    messages=Message.query.order_by(Message.created_at.asc()).all()
    return make_response(jsonify([messages.to_dict()for message in messages]),200)

@app.route('/messages',methods=['POST'])
def create_messages():
  data=request.form
  new_message=Message(
      body=data.get('body'),
      username=data.get('username')
  )
  db.session.add(new_message)
  db.session.commit()
  return make_response(new_message.to_dict(),201)

@app.route('/messages/<int:id>',methods=['PATCH'])
def messages_by_id(id):
    message = Message.query.get(id)
    if not message:
        return make_response({'error': 'Message not found'}, 404)
    
    data = request.get_json()
    if 'body' in data:
        message.body = data.get('body')
    db.session.commit()
    return make_response(message.to_dict(), 200)

@app.route('/messages/<int:id>', methods=['DELETE'])
def delete_message(id):
    message = Message.query.get(id)
    if not message:
        return make_response({'error': 'Message not found'}, 404)
    
    db.session.delete(message)
    db.session.commit()
    return make_response({'message': 'Message deleted successfully'}, 200)

if __name__ == '__main__':
    app.run(port=5555)
