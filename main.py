import json
import os
import utilities as utils
from user import User
from flask_login import LoginManager, login_required, login_user, current_user
from flask import Flask, url_for, render_template, jsonify, request

dialogue_data_path = "static/data/"
label_data_path = "static/data/labels"
user_data_path = "static/data/users"



app = Flask(__name__)
app.secret_key = os.urandom(32)
app.config['TESTING'] = False
# app.config['LOGIN_DISABLED'] = True

login_manager = LoginManager()
login_manager.init_app(app)
# login_manager.login_view = "/home"
users = dict()

dialogue_file = "test_1"
#model = utils.create_model(dialogue_data_path, dialogue_file)


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
    print(current_user.is_authenticated)
    if not current_user.is_authenticated:
        return render_template('home.html', message='Please login first!')
    return render_template('annotate.html')

# callback to reload the user object
@login_manager.user_loader
def load_user(user_id):
    return User(user_id)

@app.route('/login.do', methods=['GET', 'POST'])
def login():
    print("In login func " + request.method)
    if request.method == 'POST':
        # Todo validate username
        user_name = request.get_data(as_text=True)
        # session['user_name'] = user_name
        # print(session['user_name'])
        user = User(user_name)
        users[user_name] = user
        login_user(user)
        success = True
        # Todo get the relevant dialogue file
        # Todo create a model for the user
        user.set_model(utils.create_model(dialogue_data_path, dialogue_file, user.get_id()))
        print(user.get_model().dataset)
        return json.dumps({'success': success}), 200, {'ContentType': 'application/json'}
    return render_template('login.html')

# Dialogue View
@app.route('/get_current_dialogue.do')
def get_current_dialogue():
    print(users)
    print(current_user)
    user = users[current_user.get_id()]
    print(user)
    model = user.get_model()
    print(model.dataset)

    # Get the current dialogue from the model
    dialogue = model.get_current_dialogue()
    # Convert it to a dictionary
    current_dialogue = utils.dialogue_to_dict(dialogue)
    return jsonify(current_dialogue)


@app.route('/save_current_dialogue.do', methods=['POST'])
def save_current_dialogue():
    # Parse the request JSON
    dialogue = request.get_json()
    # Update the model with the new dialogue
    success = model.update_dialogue(dialogue)
    return json.dumps({'success': success}), 200, {'ContentType': 'application/json'}


@app.route('/get_prev_dialogue.do')
def get_prev_dialogue():
    # Increment to models next dialogue
    success = model.dec_current_dialogue()
    return json.dumps({'success': success}), 200, {'ContentType': 'application/json'}


@app.route('/get_next_dialogue.do')
def get_next_dialogue():
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
    return jsonify(labels_groups)


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=80)
