import os
from flask import Flask, render_template, redirect, url_for, request
from flask_bootstrap import Bootstrap
from flask_sqlalchemy import SQLAlchemy
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField
from wtforms.validators import DataRequired, Length
import requests

FILE_URI = 'sqlite:///movie_list.db'

app = Flask(__name__)
app.config['SECRET_KEY'] = '8BYkEfBA6O6donzWlSihBXox7C0sKR6b'
Bootstrap(app)

app.config['SQLALCHEMY_DATABASE_URI'] = FILE_URI
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)


class Movies(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), unique=True, nullable=False)
    year = db.Column(db.Integer, nullable=False)
    description = db.Column(db.String(500), nullable=False)
    rating = db.Column(db.Float, nullable=False)
    ranking = db.Column(db.Integer, nullable=False)
    review = db.Column(db.String(200), nullable=False)
    image_url = db.Column(db.String(100), nullable=False)


if not os.path.isfile(FILE_URI):
    db.create_all()


class update_form(FlaskForm):
    rating = StringField(label="Rating out of 10", validators=[DataRequired(), Length(max=200)],
                         render_kw={"autocomplete": "off"})
    review = StringField(label="Review", validators=[DataRequired(), Length(max=200)],
                         render_kw={"autocomplete": "off"})
    submit = SubmitField("update")


class add_form(FlaskForm):
    title = StringField("Movie title", validators=[DataRequired(), Length(max=100)])
    submit = SubmitField("Add Movie")


@app.route("/")
def home():
    all_movies = db.session.query(Movies).all()
    return render_template("index.html", movies=all_movies)


@app.route('/update', methods=["GET", "POST"])
def update():
    form = update_form()
    movie_id = request.args.get('id')
    movie = Movies.query.get(movie_id)
    if form.validate_on_submit():
        movie.rating = form.rating.data
        movie.review = form.review.data
        db.session.commit()
        return redirect(url_for('home'))
    return render_template('edit.html', form=form, movie=movie)


@app.route('/delete', methods=["GET", "POST"])
def delete():
    movie_id = request.args.get('id')
    movie = Movies.query.get(movie_id)
    db.session.delete(movie)
    db.session.commit()
    return redirect(url_for('home'))

@app.route('/add', methods=["GET", "POST"])
def add():
    form = add_form()
    return render_template('add.html', form=form)


if __name__ == '__main__':
    app.run(debug=True)
