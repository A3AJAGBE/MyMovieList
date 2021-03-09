from flask import Flask, render_template
from flask_bootstrap import Bootstrap

app = Flask(__name__)
Bootstrap(app)


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/add')
def add():
    return render_template('add.html')


@app.route('/edit')
def edit():
    return render_template('edit.html')


if __name__ == '__main__':
    app.run(debug=True)