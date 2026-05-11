from flask import Flask, jsonify, render_template, request
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column
from sqlalchemy import Integer, String, Boolean
import random

app = Flask(__name__)

# CREATE DB
class Base(DeclarativeBase):
    pass
# Connect to Database
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///cafes.db'
db = SQLAlchemy(model_class=Base)
db.init_app(app)


# Cafe TABLE Configuration
class Cafe(db.Model):
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    name: Mapped[str] = mapped_column(String(250), unique=True, nullable=False)
    map_url: Mapped[str] = mapped_column(String(500), nullable=False)
    img_url: Mapped[str] = mapped_column(String(500), nullable=False)
    location: Mapped[str] = mapped_column(String(250), nullable=False)
    seats: Mapped[str] = mapped_column(String(250), nullable=False)
    has_toilet: Mapped[bool] = mapped_column(Boolean, nullable=False)
    has_wifi: Mapped[bool] = mapped_column(Boolean, nullable=False)
    has_sockets: Mapped[bool] = mapped_column(Boolean, nullable=False)
    can_take_calls: Mapped[bool] = mapped_column(Boolean, nullable=False)
    coffee_price: Mapped[str] = mapped_column(String(250), nullable=True)


with app.app_context():
    db.create_all()


@app.route("/")
def home():
    return render_template("index.html")

# HTTP GET - Read Record
@app.route("/random",methods=["GET"])
def random_cafe_generator():
        all_cafes=db.session.execute(db.select(Cafe)).scalars().all()
        random_cafe=random.choice(all_cafes) #SQLAlchemy Object
        return jsonify(cafe={
            "can_take_calls": random_cafe.can_take_calls,
            "coffee_price": random_cafe.coffee_price,
            "has_sockets": random_cafe.has_sockets,
            "has_toilet": random_cafe.has_toilet,
            "has_wifi": random_cafe.has_wifi,
            "id": random_cafe.id,
            "img_url": random_cafe.img_url,
            "location": random_cafe.location,
            "map_url": random_cafe.map_url,
            "name": random_cafe.name,
            "seats": random_cafe.seats,
        })

@app.route("/all",methods=["GET"])
def cafes():
    all_cafes=db.session.execute(db.select(Cafe)).scalars().all()
    list_cafes=[]
    for cafe in all_cafes:
        list_cafes.append({
        "can_take_calls": cafe.can_take_calls,
        "coffee_price": cafe.coffee_price,
        "has_sockets": cafe.has_sockets,
        "has_toilet": cafe.has_toilet,
        "has_wifi": cafe.has_wifi,
        "id": cafe.id,
        "img_url": cafe.img_url,
        "location": cafe.location,
        "map_url": cafe.map_url,
        "name": cafe.name,
        "seats": cafe.seats,
        })
    return jsonify(cafes=list_cafes)

@app.route("/search",methods=["GET"])
def search():
    location=request.args.get("loc")
    required_cafes=db.session.execute(db.select(Cafe).where(Cafe.location==location)).scalars().all()
    if required_cafes:
        cafes=[]
        for cafe in required_cafes:
            cafes.append({
                "can_take_calls": cafe.can_take_calls,
                "coffee_price": cafe.coffee_price,
                "has_sockets": cafe.has_sockets,
                "has_toilet": cafe.has_toilet,
                "has_wifi": cafe.has_wifi,
                "id": cafe.id,
                "img_url": cafe.img_url,
                "location": cafe.location,
                "map_url": cafe.map_url,
                "name": cafe.name,
                "seats": cafe.seats,
            })
        return jsonify(cafe=cafes)
    else:
        return jsonify(error={"Not Found":"No cafes found"})



# HTTP POST - Create Record
@app.route("/add",methods=["POST"])
def add_cafe():
    new_cafe=Cafe(
        can_take_calls=request.form.get("can_take_calls"),
        coffee_price=request.form.get("coffee_price"),
        has_sockets=request.form.get("has_sockets"),
        has_toilet=request.form.get("has_toilet"),
        has_wifi=request.form.get("has_wifi"),
        id=request.form.get("id"),
        img_url=request.form.get("cafe.img_url"),
        location=request.form.get("location"),
        map_url=request.form.get("map_url"),
        name=request.form.get("name"),
        seats=request.form.get("seats"),
    )
    db.session.add(new_cafe)
    db.session.commit()
    return jsonify(response={"success":"Successfully added cafe"})


# HTTP PUT/PATCH - Update Record
@app.route("/update-price/<int:cafe_id>",methods=["PATCH"]) #pass cafe id in the url and then add new_price as a parameter in postman
def path_cafe(cafe_id):
    new_price=request.args.get("new_price")
    cafe=db.session.execute(db.select(Cafe).where(Cafe.id==cafe_id)).scalars().first()
    if cafe:
        cafe.coffee_price=new_price
        db.session.commit()
        return jsonify(success="Successfully updated price")
    else:
        return jsonify(error={"Not Found":"Sorry, a cafe with that id was not found in the database"})
# HTTP DELETE - Delete Record
@app.route("/report-closed/<int:cafe_id>",methods=["DELETE"])
def remove_cafe(cafe_id):
    api_key=request.args.get("api_key")
    if api_key=="TopSecretAPIKey":
        cafe_to_delete=db.session.execute(db.select(Cafe).where(Cafe.id==cafe_id)).scalars().first()
        if cafe_to_delete:
            db.session.delete(cafe_to_delete)
            db.session.commit()
            return jsonify(success="Successfully removed cafe")
        else:
            return jsonify(error="Cafe not found")
    else:
        return jsonify(error="Invalid API key")



if __name__ == '__main__':
    app.run(debug=True)
