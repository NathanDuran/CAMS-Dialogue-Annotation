import json

import utilities as utils
from flask import Flask, url_for, render_template, jsonify

dialogue_data_path = "static/data/"
user_data_path = "static/data/users"
label_data_path = "static/labels"
dialogue_file = "test"

model = utils.create_model(dialogue_data_path, dialogue_file)
app = Flask(__name__)


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
def annotate_page():
    return render_template('annotate.html')


# Dialogue View
@app.route('/get_current_dialogue/')
def get_current_dialogue():
    # Get the current dialogue from the model
    dialogue = model.get_current_dialogue()
    # Convert it to a dictionary
    current_dialogue = utils.dialogue_to_dict(dialogue)
    return jsonify(current_dialogue)


@app.route('/prev_dialogue/')
def prev_dialogue():
    # Increment to models next dialogue
    success = model.dec_current_dialogue()
    return str(success)


@app.route('/next_dialogue/')
def next_dialogue():
    # Increment to models next dialogue
    success = model.inc_current_dialogue()
    return str(success)


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


@app.context_processor
def example():
    return dict(myexample='This is an example')


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=80)
