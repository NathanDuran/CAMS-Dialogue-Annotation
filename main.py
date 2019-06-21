import json
import os
import utilities as utils
from user import User
from flask_login import LoginManager, login_required, login_user, logout_user, current_user
from flask import Flask, render_template, request

label_data_path = "static/labels/"
dialogue_data_path = "static/data/"
user_data_path = "static/user_data/"

app = Flask(__name__)
app.secret_key = os.urandom(32)
# app.config['TESTING'] = False
# app.config['LOGIN_DISABLED'] = True

login_manager = LoginManager()
login_manager.init_app(app)
# login_manager.login_view = "/home"
current_users = dict()
valid_users = ['usr_1', 'usr_2']  # TODO read from file


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/home')
def home_page():
    return render_template('home.html')


@app.route('/schema')
def schema_page():
    return render_template('schema.html')


@app.route('/practice')
def practice_page():
    return render_template('practice.html')


@app.route('/annotate')
# @login_required
def annotate_page():
    # If the user is not logged in then redirect with a message
    if not current_user.is_authenticated:
        return render_template('home.html', message='Please login first!')
    return render_template('annotate.html')


# callback to reload the user object
@login_manager.user_loader
def load_user(user_id):
    return User(user_id)


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
            login_user(user)

            # Get the relevant dialogue file and create a model for the user
            # If the user already has a file return that
            if os.path.isfile(user_data_path + user.get_id() + ".json"):
                dialogue_file = user.get_id()
                success = user.set_model(utils.create_model(user_data_path, dialogue_file, user.get_id()))
            # Else determine which one of the originals to return
            else:
                user_dataset = user.get_id().split('_')[1]
                dialogue_file = "set_" + user_dataset
                success = user.set_model(utils.create_model(dialogue_data_path, dialogue_file, user.get_id()))

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
    success = utils.save_model(user_data_path, model, user.get_id())
    return json.dumps({'success': success}), 200, {'ContentType': 'application/json'}


@app.route('/get_prev_dialogue.do')
def get_prev_dialogue():
    # Get the current users model
    user = current_users[current_user.get_id()]
    model = user.get_model()

    # Increment to models next dialogue
    success = model.dec_current_dialogue()
    return json.dumps({'success': success}), 200, {'ContentType': 'application/json'}


@app.route('/get_next_dialogue.do')
def get_next_dialogue():
    # Get the current users model
    user = current_users[current_user.get_id()]
    model = user.get_model()

    # Increment to models next dialogue
    success = model.inc_current_dialogue()
    return json.dumps({'success': success}), 200, {'ContentType': 'application/json'}


@app.route('/get_labels/<filename>')
def get_labels(filename):
    # Load the specified labels file
    labels_data = utils.load_txt_data(label_data_path, filename)

    # If unable to load labels inform user
    if not labels_data:
        print("unable to load label lists...")

    # Split into groups
    labels_groups = utils.load_label_groups(labels_data)
    return json.dumps(labels_groups), 200, {'ContentType': 'application/json'}


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=80)
