from flask import Flask, render_template, redirect, url_for, request
from flask_bootstrap import Bootstrap5
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column
from sqlalchemy import Integer, String, Float
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField,FloatField
from wtforms.validators import DataRequired
import requests

class EditForm(FlaskForm):
    new_rating=FloatField('Your rating out of 10 (eg: 7.5) ',validators=[DataRequired()])
    new_review=StringField('Your review',validators=[DataRequired()])
    submit=SubmitField('Done')

class AddForm(FlaskForm):
    anime=StringField('Enter Anime name',validators=[DataRequired()])
    submit=SubmitField('Add anime')

app = Flask(__name__)
app.config['SECRET_KEY'] = '8BYkEfBA6O6donzWlSihBXox7C0sKR6b'
Bootstrap5(app)


# CREATE DB
class Base(DeclarativeBase):
    pass


db = SQLAlchemy(model_class=Base)
app.config['SQLALCHEMY_DATABASE_URI'] = "sqlite:///animes.db"
db.init_app(app)


class Animes(db.Model):
    id: Mapped[int] = mapped_column(primary_key=True)
    title: Mapped[str] = mapped_column(nullable=False, unique=True)
    year: Mapped[int] = mapped_column(nullable=False)
    description: Mapped[str] = mapped_column(nullable=False)
    rating: Mapped[float] = mapped_column(nullable=True)
    ranking: Mapped[int] = mapped_column(nullable=True)
    review: Mapped[str] = mapped_column(nullable=True)
    img_url: Mapped[str] = mapped_column(nullable=False)


# CREATE TABLE
with app.app_context():
    db.create_all()

    db.session.commit()

@app.route("/")
def home():
    all_animes=db.session.execute(db.select(Animes).order_by(Animes.rating)).scalars().all()
    return render_template("index.html",all_animes=all_animes)

@app.route("/edit/<int:id>",methods=["GET","POST"])
def edit(id):
    form=EditForm()
    if form.validate_on_submit():
        new_rating=form.new_rating.data
        new_review=form.new_review.data
        anime=db.session.execute(
            db.select(Animes).where(Animes.id==id)
        ).scalar()
        anime.rating=new_rating
        anime.review=new_review
        db.session.commit()
        return redirect(url_for("home"))
    anime=db.session.execute(db.select(Animes).where(Animes.id==id)).scalar()
    return render_template("edit.html",anime=anime,form=form)

@app.route("/delete/<int:id>")
def delete(id):
    anime=db.session.execute(db.select(Animes).where(Animes.id==id)).scalar()
    db.session.delete(anime)
    db.session.commit()
    return redirect(url_for("home"))


@app.route("/add",methods=["GET","POST"])
def add():
    form=AddForm()
    if form.validate_on_submit():
        anime_name=form.anime.data
        response=requests.get("https://api.jikan.moe/v4/anime",params={"q":anime_name,"limit":1})
        data=response.json()
        anime=data["data"][0]
        new_anime=Animes(
            title=anime["title"],
            year = anime["year"],
            description = anime["synopsis"],
            img_url = anime["images"]["jpg"]["image_url"],
        )
        db.session.add(new_anime)
        db.session.commit()
        return redirect(url_for("edit",id=new_anime.id))
    return render_template("add.html",form=form)
if __name__ == '__main__':
    app.run(debug=True)
