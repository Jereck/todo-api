from flask import Blueprint, request, jsonify
from app import db
from app.models import User, Todo
from flask_jwt_extended import create_access_token, jwt_required, get_jwt_identity

auth_bp = Blueprint("auth", __name__)
todo_bp = Blueprint("todo", __name__)

# User Registration
@auth_bp.route("/register", methods=["POST"])
def register():
    data = request.get_json()
    if not data.get("username") or not data.get("password"):
        return jsonify({"error": "Username and password required"}), 400
    
    if User.query.filter_by(username=data["username"]).first():
        return jsonify({"error": "User already exists"}), 400
    
    user = User(username=data["username"])
    user.set_password(data["password"])
    db.session.add(user)
    db.session.commit()
    
    return jsonify({"message": "User registered successfully"}), 201

# User Login
@auth_bp.route("/login", methods=["POST"])
def login():
    data = request.get_json()
    user = User.query.filter_by(username=data["username"]).first()
    
    if user and user.check_password(data["password"]):
        access_token = create_access_token(identity=str(user.id))
        return jsonify({"access_token": access_token}), 200

    return jsonify({"error": "Invalid credentials"}), 401

# Get All Todos (Protected)
@todo_bp.route("/", methods=["GET"])
@jwt_required()
def get_todos():
    user_id = get_jwt_identity()
    todos = Todo.query.filter_by(user_id=user_id).all()
    return jsonify([{"id": t.id, "title": t.title, "description": t.description, "done": t.done, "user_id": t.user_id} for t in todos])

# Create a Todo
@todo_bp.route("/", methods=["POST"])
@jwt_required()
def create_todo():
    user_id = get_jwt_identity()
    data = request.get_json()
    
    if not data.get("title"):
        return jsonify({"error": "Title is required"}), 400
    
    todo = Todo(title=data["title"], description=data["description"], user_id=user_id)
    db.session.add(todo)
    db.session.commit()
    
    return jsonify({"message": "Todo created"}), 201

# Update a Todo
@todo_bp.route("/<int:todo_id>", methods=["PUT"])
@jwt_required()
def update_todo(todo_id):
    user_id = get_jwt_identity()
    todo = Todo.query.get(todo_id)
    
    if not todo or todo.user_id != user_id:
        return jsonify({"error": "Todo not found"}), 404

    data = request.get_json()
    todo.title = data.get("title", todo.title)
    todo.completed = data.get("completed", todo.completed)
    
    db.session.commit()
    return jsonify({"message": "Todo updated"}), 200

# Delete a Todo
@todo_bp.route("/<int:todo_id>", methods=["DELETE"])
@jwt_required()
def delete_todo(todo_id):
    user_id = get_jwt_identity()
    todo = Todo.query.get(todo_id)
    
    if not todo or todo.user_id != user_id:
        return jsonify({"error": "Todo not found"}), 404
    
    db.session.delete(todo)
    db.session.commit()
    return jsonify({"message": "Todo deleted"}), 200
