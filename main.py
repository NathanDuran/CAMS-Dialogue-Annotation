import file_utilities as utils
from flask import Flask, url_for, render_template, jsonify

json_data_path = "static/data/"
label_data_path = "static/labels"

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


@app.route('/get_dialogue/<filename>')
def get_dialogue(filename):

    json_data = utils.load_json_data(json_data_path, filename)
    return jsonify(json_data)


@app.route('/get_labels/<filename>')
def get_labels(filename):

    # Load the specified labels file
    labels_data = utils.load_txt_data(label_data_path, filename)
    # Split into groups
    labels_groups = utils.split_label_groups(labels_data)
    return jsonify(labels_groups)


@app.context_processor
def example():
    return dict(myexample='This is an example')


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=80)