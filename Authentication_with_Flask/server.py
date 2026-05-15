from flask import Flask, render_template, request, url_for, redirect, flash, send_from_directory
from werkzeug.security import generate_password_hash, check_password_hash
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column
from sqlalchemy import Integer, String
from flask_login import UserMixin, login_user, LoginManager, login_required, current_user, logout_user
import os
from dotenv import load_dotenv

load_dotenv()

app = Flask(__name__)
app.config['SECRET_KEY'] = os.getenv('SECRET_KEY')

# CREATE DATABASE
class Base(DeclarativeBase):
    pass


app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///users.db'
db = SQLAlchemy(model_class=Base)
db.init_app(app)

# CREATE TABLE IN DB
class User(UserMixin,db.Model):
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    email: Mapped[str] = mapped_column(String(100), unique=True)
    password: Mapped[str] = mapped_column(String(100))
    name: Mapped[str] = mapped_column(String(1000))


with app.app_context():
    db.create_all()


login_manager=LoginManager()
login_manager.init_app(app)
# login_manager.login_view='login'

@login_manager.user_loader
def load_user(user_id):
    return db.session.get(User,user_id)

# @login_manager.unauthorized_handler
# def unauthorized():
#     flash("Please login to access this page")
#     return redirect(url_for('login'))



@app.route('/')
def home():
    return render_template("index.html")


@app.route('/register',methods=['POST','GET'])
def register():
    if request.method=='POST':
        name=request.form['name']
        email=request.form['email']
        check_user_exists=db.session.execute(db.select(User).where(User.email==email)).scalars().first()
        if check_user_exists:
            flash(f"You've already signed up with that email, please login instead.")
            return redirect(url_for('login'))
        hashed_salted_password=generate_password_hash(request.form['password'],method='pbkdf2:sha256:600000',salt_length=8)
        new_user=User(
            name=name,
            email=email,
            password=hashed_salted_password,
        )
        db.session.add(new_user)
        db.session.commit()
        login_user(new_user)
        return redirect(url_for('secrets',name=name)) #Pass name to route

    else:
        return render_template("register.html")

@app.route('/login',methods=['POST','GET'])
def login():
    if request.method=='POST':
        email=request.form['email']
        password=request.form['password']
        user_object=db.session.execute(db.select(User).where(User.email==email)).scalars().first()
        if user_object:
            pwhash=user_object.password
            if check_password_hash(pwhash,password):
                login_user(user_object)
                return redirect(url_for('secrets',name=user_object.name))
            else:
                flash('Login Unsuccessful. Please check password')
                return redirect(url_for('login'))
        else:
            flash('Login Unsuccessful. Email not registered')
            return redirect(url_for('login'))
    else:
        return render_template("login.html")


@app.route('/secrets')
@login_required
def secrets():
    return render_template("secrets.html",name=current_user.name)#Pass name from route to file


@app.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('home'))


@app.route('/download')
@login_required
def download():
    return send_from_directory('static/files','cheat_sheet.pdf',as_attachment=True)


if __name__ == "__main__":
    app.run(debug=True)
