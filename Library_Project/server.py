from flask import Flask, render_template, request,redirect,url_for
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column

class Base(DeclarativeBase):
    pass

db=SQLAlchemy(model_class=Base)
app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI']='sqlite:///library.db'
db.init_app(app)

class Books(db.Model):
    id:Mapped[int]=mapped_column(primary_key=True)
    title:Mapped[str]=mapped_column(nullable=False,unique=True)
    author:Mapped[str]=mapped_column(nullable=False)
    rating:Mapped[float]=mapped_column(nullable=False)

with app.app_context():
    db.create_all()


@app.route('/')
def home():
    all_books=db.session.execute(db.select(Books)).scalars().all()
    #.scalars().all() immediately fetches all records into a Python list.
    return render_template('index.html',books=all_books)


@app.route("/add",methods=['POST','GET'])
def add():
    if request.method=='POST': #Get the data from the form when request is POST
        book_name=request.form['bookname']
        author=request.form['author']
        rating=request.form['rating']
        new_book=Books(
            title=book_name,
            author=author,
            rating=rating,
        )
        db.session.add(new_book)
        db.session.commit()
        return redirect(url_for('home'))
    return render_template('add.html') #Render when request is GET


@app.route('/edit/<int:id>',methods=['GET','POST'])
def edit(id):
    book_to_update=db.session.execute(db.select(Books).where(Books.id==id)).scalar()
    if request.method=='POST':
        book_to_update.rating=request.form['new_rating']
        db.session.commit()
        return redirect(url_for('home'))
    else:
        return render_template('edit.html',book_to_update=book_to_update)

@app.route('/delete/<int:id>')
def delete(id):
    book_to_delete=db.session.execute(db.select(Books).where(Books.id==id)).scalar()
    db.session.delete(book_to_delete)
    db.session.commit()
    return redirect(url_for('home'))

if __name__ == "__main__":
    app.run(debug=True)

