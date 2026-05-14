from flask import Flask, render_template, redirect, url_for,request
from flask_bootstrap import Bootstrap5
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column
from sqlalchemy import Integer, String, Text
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField
from wtforms.validators import DataRequired, URL
from flask_ckeditor import CKEditor, CKEditorField
from datetime import date

app = Flask(__name__)
app.config['SECRET_KEY'] = '8BYkEfBA6O6donzWlSihBXox7C0sKR6b'
Bootstrap5(app)
ckeditor=CKEditor(app)

#FORM USING WTFORMS
class NewPostForm(FlaskForm):
    title=StringField('Blog Post Title',validators=[DataRequired()])
    subtitle=StringField('Subtitle',validators=[DataRequired()])
    author=StringField('Your Name',validators=[DataRequired()])
    img_url=StringField('Blog Image URL',validators=[DataRequired()])
    body=CKEditorField('Blog content',validators=[DataRequired()])
    submit=SubmitField('Submit')



# CREATE DATABASE
class Base(DeclarativeBase):
    pass
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///posts.db'
db = SQLAlchemy(model_class=Base)
db.init_app(app)


# CONFIGURE TABLE
class BlogPost(db.Model):
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    title: Mapped[str] = mapped_column(String(250), unique=True, nullable=False)
    subtitle: Mapped[str] = mapped_column(String(250), nullable=False)
    date: Mapped[str] = mapped_column(String(250), nullable=False)
    body: Mapped[str] = mapped_column(Text, nullable=False)
    author: Mapped[str] = mapped_column(String(250), nullable=False)
    img_url: Mapped[str] = mapped_column(String(250), nullable=False)


with app.app_context():
    db.create_all()

#Getting date
date_=date.today()
formatted_date=date_.strftime("%B %d, %Y")

@app.route('/')
def get_all_posts():
    posts = db.session.execute(db.select(BlogPost)).scalars().all() #Returns a list of BlogPost objects
    return render_template("index.html", all_posts=posts)

@app.route('/<int:post_id>')
def show_post(post_id):
    requested_post = db.session.execute(db.select(BlogPost).where(BlogPost.id==post_id)).scalars().first()
    return render_template("post.html", post=requested_post)


# TODO: add_new_post() to create a new blog post
@app.route('/new-post',methods=['POST','GET'])
def new_post():
    form=NewPostForm()
    if request.method=='POST':
        title=request.form['title']
        subtitle=request.form['subtitle']
        author=request.form['author']
        img_url=request.form['img_url']
        body=request.form['body']
        new_post=BlogPost(
            title=title,
            subtitle=subtitle,
            author=author,
            img_url=img_url,
            body=body,
            date=formatted_date,
        )
        db.session.add(new_post)
        db.session.commit()
        return redirect(url_for('get_all_posts'))
    else:
        return render_template("make-post.html",form=form,reason='new post')



# TODO: edit_post() to change an existing blog post
@app.route("/edit-post/<int:post_id>",methods=['GET','POST'])
def edit_post(post_id):
    post = db.session.execute(db.select(BlogPost).where(BlogPost.id == post_id)).scalars().first()
    if request.method=='GET':
        form1=NewPostForm(
            title=post.title,
            subtitle=post.subtitle,
            author=post.author,
            img_url=post.img_url,
            body=post.body,
            date=formatted_date,
        )
        return render_template("make-post.html",reason='editing',form=form1)
    else:
        post.title = request.form['title']
        post.subtitle = request.form['subtitle']
        post.author = request.form['author']
        post.img_url = request.form['img_url']
        post.body = request.form['body']
        db.session.commit()
        return redirect(url_for('get_all_posts'))


# TODO: delete_post() to remove a blog post from the database
@app.route('/delete-post/<int:post_id>')
def delete_post(post_id):
    post_to_delete=db.session.execute(db.select(BlogPost).where(BlogPost.id==post_id)).scalars().first()
    db.session.delete(post_to_delete)
    db.session.commit()
    return redirect(url_for('get_all_posts'))

# Below is the code from previous lessons. No changes needed.
@app.route("/about")
def about():
    return render_template("about.html")


@app.route("/contact")
def contact():
    return render_template("contact.html")


if __name__ == "__main__":
    app.run(debug=True, port=5003)
