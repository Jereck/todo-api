from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_jwt_extended import JWTManager
from dotenv import load_dotenv
import os

load_dotenv()

db = SQLAlchemy()
migrate = Migrate()
jwt = JWTManager()

def create_app():
  app = Flask(__name__)

  app.config.from_object("config.Config")

  db.init_app(app)
  migrate.init_app(app, db)
  jwt.init_app(app)

  from app.routes import todo_bp, auth_bp
  app.register_blueprint(todo_bp, url_prefix="/api/todos")
  app.register_blueprint(auth_bp, url_prefix="/api/auth")

  return app