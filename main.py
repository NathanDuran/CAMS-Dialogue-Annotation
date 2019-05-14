from flask import Flask, url_for, render_template

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

@app.context_processor
def example():
    return dict(myexample='This is an example')

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=80)