from flask import Flask, url_for, render_template

app = Flask(__name__)


@app.route('/')
def index():
    return render_template('index.html')

@app.route('/nav-bar.html')
def nav_bar():
    return render_template('nav-bar.html')

@app.route('/hello/<name>')
def hello(name):
    return render_template('hello.html', name=name)


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=80)