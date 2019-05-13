from flask import Flask, url_for, render_template

app = Flask(__name__)


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/nav-bar')
def nav_bar():
    return render_template('nav-bar.html')


@app.route('/Schema')
def schema_page():
    return render_template('schema.html')


@app.route('/Practice')
def practice_page():
    return render_template('practice.html')


@app.route('/Help')
def help_page():
    return render_template('help.html')


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=80)