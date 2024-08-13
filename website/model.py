from . import db

class Admin(db.Model):
    __tablename__ = "admin"

    id = db.Column("id", db.Integer, primary_key=True, nullable=False)
    Admin = db.Column("Admin", db.String(100), nullable=False)
    Status = db.Column("Status", db.String, default=False)
    Seed = db.Column("Seed", db.Integer, nullable=False ,default=-1)

class Dead_people(db.Model):
    __tablename__ = "dead_people"
    
    id = db.Column("id", db.Integer, primary_key=True, nullable=False)
    names = db.Column("names", db.String(100), nullable=False)
    killer = db.Column("killer", db.String(100), nullable=False)
    time_died = db.Column("time_died", db.Integer, nullable=False)
    
class Items(db.Model):
    __tablename__ = "items"

    id = db.Column("id", db.Integer, primary_key=True, nullable=False)
    item_name = db.Column("item_name", db.String(100), nullable=False)
    description = db.Column("description", db.String(100), nullable=False)
    availability = db.Column("availability", db.Integer, nullable=False ,default=1)

class People(db.Model):
    __tablename__ = "people"
    
    id = db.Column("id", db.Integer, primary_key=True, nullable=False)
    name = db.Column("name", db.String(100), nullable=False)
    status = db.Column("status", db.String(100), nullable=False, default="alive")
    items_use = db.Column("items_use", db.String(100), nullable=False, default="")
    
class Picked_characters(db.Model):
    __tablename__ = "picked_characters"

    id = db.Column("id", db.Integer, primary_key=True, nullable=False)
    name = db.Column("name", db.String(100), nullable=False)
    count = db.Column("count", db.Integer, nullable=False, default=0)
    
class Picked_names(db.Model):
    __tablename__ = "picked_names"
    
    id = db.Column("id", db.Integer, primary_key=True)
    name = db.Column("name", db.String(100), nullable=False)
    count = db.Column("count", db.Integer, nullable=False, default=0)
    time_picked = db.Column("time_picked", db.Integer, nullable=False)
    
class Teams(db.Model):
    __tablename__ = "teams"

    id = db.Column("id", db.Integer, primary_key=True)
    team_name = db.Column("team_name", db.String(100), nullable=False)
    member_name = db.Column("member_name", db.String(100), nullable=False)
    
   
    