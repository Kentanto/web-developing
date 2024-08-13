from flask import Flask
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()
DB_NAME = "deathgamecharacters.db"

def init_game():
    game = Flask(__name__)
    game.config["SECRET_KEY"] = "ye atomic's pretty good"
    game.config['SQLALCHEMY_DATABASE_URI'] = f'sqlite:///{DB_NAME}'
    db.init_app(game)
    
    from .views import head
    game.register_blueprint(head, url_prefix='/')
        
    return game