from flask import Blueprint, render_template, request, jsonify #Why tf is flask yellow???? Everything is working fine so stop being angry at me you yello fuck
from .model import Admin, Dead_people, Items, People, Picked_characters, Picked_names, Teams
from . import db
from datetime import datetime
import random
head = Blueprint("head", __name__)

@head.route("/")
def home():
    #Load what should be on the home page
    picked_people = Picked_names.query.order_by(Picked_names.time_picked.desc()).all()

    if not picked_people:
        most_recent_people = []
        
    else:
        grouped_people = {}
        for person in picked_people:
            time_key = person.time_picked
            
            if time_key not in grouped_people:
                grouped_people[time_key] = []
                
            grouped_people[time_key].append(person)
            
        most_recent_time = max(grouped_people.keys())
        most_recent_people = grouped_people[most_recent_time]
        
    return render_template("index.html", picked_people_data=most_recent_people)

@head.route("/cursed_home")
def cursed_home():
    #Kinda self explanatory
    return render_template("cursed/cursed_home.html")

@head.route("/admin")
def view_admin():
    #Some random info
    admin = Admin.query.all()
    return render_template("db_template/admin.html", admin=admin)

@head.route("/dead_people")
def view_dead_people():
    #Shows legit nothing, it doesnt exist on the page since people does this on the page already prolly gonna remove it maaaaaaybe if i feel like it
    dead = Dead_people.query.all()
    return render_template("db_template/dead_people.html", dead=dead)

@head.route("/items")
def view_items():
    #Just all items and their info
    items = Items.query.all()
    return render_template("db_template/items.html", items=items)

@head.route("/people")
def view_people():
    #Shows everythin on a person
    people = People.query.all()
    return render_template("db_template/people.html", people=people)

@head.route("/picked_names")
def view_picked_names():
    #Shows most recent pick and is used by other function to get the most recent pick on home page
    picked_names = Picked_names.query.order_by(Picked_names.time_picked.desc()).all()
    return render_template("db_template/picked_names.html", picked_names=picked_names)

@head.route("/teams")
def view_teams():
    #Nuffin yet
    teams = Teams.query.all()
    return render_template("db_template/teams.html", teams=teams)





@head.route("/check_modfiy_person", methods=["POST"])
def check_or_modify():
    #Function to check and or change info on a character
        person_name = request.form["person_name"]
        modify_person = request.form.get("modify_person")
        modification_type = request.form.get("modification_type")
        additional_info = request.form.get("additional_info")

        person = People.query.filter_by(name=person_name).first()
        if person:
            if modify_person == "yes":
                if modification_type in ["alive", "disabled"]:
                    person.status = modification_type
                    dead_person = Dead_people.query.filter_by(names=person_name).first()
                    if dead_person:
                        db.session.delete(dead_person)
                    db.session.commit()
                elif modification_type == "injured":
                        person.status = f"{modification_type} by: {additional_info}"
                        db.session.commit()
                elif modification_type == "Custom":
                        person.status = additional_info
                        db.session.commit()
        
        return jsonify({'message': 'Success'})

@head.route("/kill_person", methods=["POST"])
def kill_Person():
    #Do i need to explain?
    person_to_kill = request.form["target_person"]
    killer = request.form["killer"]
    person_to_die = People.query.filter_by(name=person_to_kill).first()
    if person_to_die:
        person_to_die.status = f"dead: ({killer})"
        person_to_die.items_use = ""
        dead_person_entry = Dead_people(names=person_to_kill, killer=killer, time_died=datetime.now())
        db.session.add(dead_person_entry)
        db.session.commit()
    return jsonify({'message': 'Success'})

@head.route("/get_person_info", methods=["POST"])
def get_person_info():
    #I have no clue what this does, but it works. It's prolly important
    person_name = request.json["person_name"]
    if person_name:
        person = People.query.filter_by(name=person_name).first()
        if person:
            html = f"<p>Name: {person.name}</p>"
            html += f"<p>Status: {person.status}</p>"
            html += f"<p>Items Use: {person.items_use}</p>"
            return jsonify({"html": html})
        else:
            return jsonify({"html": "<p>Person not found</p>"})
        
    
@head.route("/pick_people", methods=["POST"])
def pick_people():
    #Again do i really need to?
    Picked_People = []
    alive_people = People.query.filter_by(status="alive").all()

    num_to_pick = random.randint(2, 3)
    picked_people = random.sample(alive_people, num_to_pick)
    for person in picked_people:
        picked_character = Picked_names.query.filter_by(name=person.name).first()
        if picked_character:
            picked_character.count += 1
            picked_character.time_picked = datetime.now().replace(microsecond=0)
        else:
            new_picked_character = Picked_names(name=person.name, count=1, time_picked=datetime.now().replace(microsecond=0))
            db.session.add(new_picked_character)
        
        Picked_People.append({
        "name":person.name,
        "status": person.status,
        "items_use": person.items_use})
        db.session.commit()
    
    return jsonify(Picked_People)



def wagner_fischer(s1, s2):
    len_s1, len_s2 = len(s1), len(s2)
    if len_s1 > len_s2:
        s1, s2 = s2, s1
        len_s1, len_s2 = len_s2, len_s1

    current_row = range(len_s1 + 1)
    for i in range(1, len_s2 + 1):
        previous_row, current_row = current_row, [i] + [0] * len_s1
        for j in range(1, len_s1 + 1):
            add, delete, change = previous_row[j] + 1, current_row[j-1] + 1, previous_row[j-1]
            if s1[j-1] != s2[i-1]:
                change += 1
            current_row[j] = min(add, delete, change)

    return current_row[len_s1]


@head.route("/spell_check", methods=["POST"])
def spell_check():
    word = request.form.get("word")
    dictionary = People.query.with_entities(People.name).all()
    suggestions = []

    for row in dictionary:
        correct_word = row[0]
        distance = wagner_fischer(word, correct_word)
        suggestions.append((correct_word, distance))

    suggestions.sort(key=lambda x: x[1])
    return jsonify({"suggestions": suggestions[:1]})

@head.route("/reset_game", methods=["post"] )
def reset_game():
    item_availability = {
    "Tail wag of doom": 2,
    "Yawn of doom": 2,
    "Mystery game": 1,
    "God's mercy": 1,
    "D'baguette": 1,
    "Eh'Syrup": 1,
    "Raphael": 1,
    "Atomic's curse": 1,
    "Button of doom": 2,
    "Senseless cloak": 1,
    "Air strike of doom": 1,
    "talk no jutsu": 1,
    "Goal-post of doom": 1,
    "Open net": 1,
    "120 Ping": 1
    }

    new_seed = random.randint(1, 1000000)
    admin_record = Admin.query.first()
    admin_record.Seed = new_seed
    Dead_people.query.delete()
    items = Items.query.all()
    for item in items:
        if item.item_name in item_availability:
            item.availability = item_availability[item.item_name]
    people = People.query.all()
    for person in people:
        person.status = "alive"
        person.items_use = ""        
    Picked_characters.query.delete()
    Picked_names.query.delete()
    Teams.query.delete()        
    db.session.commit()
    
    return render_template("index.html")