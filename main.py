import os
from flask import Flask, render_template, redirect, url_for, request
from flask_bootstrap import Bootstrap
from flask_sqlalchemy import SQLAlchemy
from flask_wtf import FlaskForm
from wtforms import StringField, IntegerField, FloatField, SubmitField
from wtforms.validators import DataRequired, url
from dotenv import load_dotenv

load_dotenv()


app = Flask(__name__)
Bootstrap(app)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///movies-collection.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)
app.secret_key = os.environ.get('SECRET_KEY')


class Movies(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(250), unique=True, nullable=False)
    year = db.Column(db.Integer, nullable=False)
    description = db.Column(db.String(250), nullable=False)
    rating = db.Column(db.Float, nullable=False)
    ranking = db.Column(db.Integer, nullable=False)
    review = db.Column(db.String(250), nullable=False)
    image_url = db.Column(db.String(250), nullable=False)

    def __repr__(self):
        return f'Movie Title: {self.title}'


db.create_all()


class MovieForm(FlaskForm):
    title = StringField('Title', validators=[DataRequired()])
    year = IntegerField('Year', validators=[DataRequired()])
    description = StringField('Description', validators=[DataRequired()])
    rating = FloatField('Personal Rating Out of 10 e.g. 7.5', validators=[DataRequired()])
    ranking = IntegerField('Personal Ranking', validators=[DataRequired()])
    review = StringField('Personal Review', validators=[DataRequired()])
    image = StringField('Image Url', validators=[DataRequired(), url()])
    submit = SubmitField('Submit')


class RateMovieForm(FlaskForm):
    rating = FloatField('Personal Rating Out of 10 e.g. 7.5', validators=[DataRequired()])
    review = StringField('Personal Review', validators=[DataRequired()])
    submit = SubmitField('Submit')


@app.route('/')
def index():
    all_movies = Movies.query.order_by(Movies.rating).all()

    for i in range(len(all_movies)):
        # This line gives each movie a new ranking reversed from their order in all_movies
        all_movies[i].ranking = len(all_movies) - i
    return render_template('index.html', movies=all_movies)


@app.route('/add', methods=["GET", "POST"])
def add():
    form = MovieForm()
    if request.method == 'POST':
        new_movie = Movies(
            title=request.form['title'],
            year=request.form['year'],
            description=request.form['description'],
            rating=request.form['rating'],
            ranking=request.form['ranking'],
            review=request.form['review'],
            image_url=request.form['image'])
        db.session.add(new_movie)
        db.session.commit()
        return redirect(url_for('index'))
    return render_template('add.html', form=form)


@app.route('/edit/<int:movie_id>', methods=["GET", "POST"])
def edit(movie_id):
    form = RateMovieForm()
    movie_edit = Movies.query.get(movie_id)
    if request.method == 'POST':
        movie_edit.rating = request.form['rating']
        movie_edit.review = request.form['review']
        db.session.commit()
        return redirect(url_for('index'))
    return render_template('edit.html', form=form, movie=movie_edit)


@app.route('/delete/<int:movie_id>')
def delete(movie_id):
    delete_movie = Movies.query.get(movie_id)
    db.session.delete(delete_movie)
    db.session.commit()
    return redirect(url_for('index'))


if __name__ == '__main__':
    app.run(debug=True)
