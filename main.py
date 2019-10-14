import json
import os
import utilities as utils
from user import User
from flask_login import LoginManager, login_required, login_user, logout_user, current_user
from flask import Flask, render_template, request

app = Flask(__name__)
app.secret_key = os.urandom(32)

login_manager = LoginManager()
login_manager.init_app(app)

data_path = "static/data/"
# data_path = "/home/NuDelta/mysite/static/data" # For Python Anywhere
label_data_path = os.path.join(data_path, "labels/")
dialogue_data_path = os.path.join(data_path, "dialogues/")
user_data_path = os.path.join(data_path, "user_dialogues/")

# Load the valid user list
valid_users = utils.load_txt_data(data_path, "user_id_list")
current_users = dict()


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/home')
def home_page():
    return render_template('home.html')


@app.route('/login')
def practice_page():
    return render_template('login.html')


@app.route('/schema')
def schema_page():
    return render_template('schema.html')


@app.route('/annotate')
# @login_required
def annotate_page():
    # If the user is not logged in then redirect with a message
    if not current_user.is_authenticated:
        return render_template('login.html', message='Please login first!')
    return render_template('annotate.html')


# callback to reload the user object
@login_manager.user_loader
def load_user(user_id):

    if user_id in current_users:
        return current_users[user_id]
    else:
        return None


@app.route('/login.do', methods=['POST'])
def login():
    success = False
    if request.method == 'POST':

        user_name = request.get_data(as_text=True)
        # If the user is valid and not already logged in
        if user_name in valid_users and user_name not in current_users.keys():

            # Create user and add to list
            user = User(user_name)
            current_users[user_name] = user

            # Login the user
            login_user(user, remember=True)

            # Get the relevant dialogue file and create a model for the user
            # If the user already has a file return that
            if os.path.isfile(user_data_path + user.get_id() + ".json"):
                dialogue_file = user.get_id()
                json_data = utils.load_json_data(user_data_path, dialogue_file)
                model = utils.create_model(dialogue_data_path, json_data, user.get_id(), user_data=True)
                success = user.set_model(model)

            # Else determine which one of the originals to return
            else:
                user_dataset = user.get_id().split('-')[1]
                dialogue_file = "set_" + user_dataset
                json_data = utils.load_json_data(dialogue_data_path, dialogue_file)
                model = utils.create_model(dialogue_data_path, json_data, user.get_id(), user_data=False)
                success = user.set_model(model)

    return json.dumps({'success': success}), 200, {'ContentType': 'application/json'}


@app.route('/logout.do')
@login_required
def logout():

    # Get the user to be logged out and remove from current users
    user_name = current_user.user_name
    del current_users[user_name]

    # Log them out
    success = logout_user()

    return json.dumps({'success': success, 'user_name': user_name}), 200, {'ContentType': 'application/json'}


# Dialogue View
@app.route('/get_current_dialogue.do')
def get_current_dialogue():
    # Get the current users model
    user = current_users[current_user.get_id()]
    model = user.get_model()

    # Get the current dialogue from the model
    dialogue = model.get_current_dialogue()

    # Convert it to a dictionary
    current_dialogue = utils.dialogue_to_dict(dialogue)

    # Build the response object
    dialogue_data = dict({'dataset': model.dataset,
                          'num_dialogues': model.num_dialogues,
                          'num_complete': model.num_complete,
                          'current_dialogue': current_dialogue,
                          'current_dialogue_index': model.current_dialogue_index})

    return json.dumps(dialogue_data), 200, {'ContentType': 'application/json'}


@app.route('/save_current_dialogue.do', methods=['POST'])
def save_current_dialogue():
    # Get the current users model
    user = current_users[current_user.get_id()]
    model = user.get_model()

    # Parse the request JSON
    dialogue_data = request.get_json()

    # Convert dialogue JSON/Dict to dialogue object
    dialogue = utils.dialogue_from_dict(dialogue_data)

    # Update the model with the new dialogue
    model.set_dialogue(dialogue)

    # Save to the users JSON file
    model_dict = utils.model_to_dict(model)

    success = utils.save_json_data(user_data_path, current_user.get_id(), model_dict)

    return json.dumps({'success': success}), 200, {'ContentType': 'application/json'}


@app.route('/get_prev_dialogue.do', methods=['POST'])
def get_prev_dialogue():
    # Get the current users model
    user = current_users[current_user.get_id()]
    model = user.get_model()

    # Parse the request JSON
    dialogue_data = request.get_json()

    # Convert dialogue JSON/Dict to dialogue object
    dialogue = utils.dialogue_from_dict(dialogue_data)

    # Update the model with the new dialogue
    model.set_dialogue(dialogue)

    # Increment to models next dialogue
    model.dec_current_dialogue()

    # Save to the users JSON file
    model_dict = utils.model_to_dict(model)

    success = utils.save_json_data(user_data_path, current_user.get_id(), model_dict)

    return json.dumps({'success': success}), 200, {'ContentType': 'application/json'}


@app.route('/get_next_dialogue.do', methods=['POST'])
def get_next_dialogue():
    # Get the current users model
    user = current_users[current_user.get_id()]
    model = user.get_model()

    # Parse the request JSON
    dialogue_data = request.get_json()

    # Convert dialogue JSON/Dict to dialogue object
    dialogue = utils.dialogue_from_dict(dialogue_data)

    # Update the model with the new dialogue
    model.set_dialogue(dialogue)

    # Increment to models next dialogue
    model.inc_current_dialogue()

    # Save to the users JSON file
    model_dict = utils.model_to_dict(model)

    success = utils.save_json_data(user_data_path, current_user.get_id(), model_dict)

    return json.dumps({'success': success}), 200, {'ContentType': 'application/json'}


@app.route('/get_labels.do')
def get_labels():
    # Load the labels files
    labels = utils.load_json_data(label_data_path, "labels")

    # If unable to load labels inform user
    if not labels:
        print("unable to load label lists...")

    # Return as json/dict
    return json.dumps(labels), 200, {'ContentType': 'application/json'}


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=2000)  # Default 0.0.0.0:80
