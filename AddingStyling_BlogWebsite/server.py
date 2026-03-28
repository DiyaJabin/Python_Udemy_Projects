from flask import Flask,render_template,request
import requests
import smtplib
import os
from dotenv import load_dotenv

load_dotenv()
app=Flask(__name__)

#-------CONSTANTS--------
JSON_BIN_ENDPOINT="https://api.npoint.io/691d0e7aa29fd76f3ef5"
EMAIL=os.getenv("MAIL_ADDRESS")
PASSWORD=os.getenv("MAIL_PASSWORD")

response=requests.get(JSON_BIN_ENDPOINT)
content = response.json()



@app.route('/')
def homepage():
    return render_template("index.html",heading="Anime Insight",subheading="Exploring stories, characters, and emotions beyond the screen",
                           image="background-image: url('../static/assets/img/home-bg.jpg",posts=content)

@app.route('/about')
def about():
    return render_template("about.html",heading="About Me",subheading="This is what I do",
                           image="background-image: url('../static/assets/img/about-bg.jpg")

@app.route('/contact',methods=['GET','POST'])
def contact():
    if request.method =="GET":
        return render_template("contact.html",heading="Contact Me",subheading="Have questions? I have answers",
                           image="background-image: url('../static/assets/img/contact-bg.jpg")
    else:
        name = request.form['name']
        email = request.form['email']
        phone = request.form['phone']
        message = request.form['message']
        with smtplib.SMTP('smtp.gmail.com',587) as connection:
            connection.starttls()
            connection.login(user=EMAIL,password=PASSWORD)
            connection.sendmail(
                from_addr=EMAIL,
                to_addrs=EMAIL,
                msg=f"Subject:You got a message!!\n\nName: {name}\nEmail: {email}\nPhone: {phone}\nMessage: {message}"
            )
        return render_template("form_entry.html")


@app.route('/post/<int:num>')
def post(num):
    head=''
    subhead=''
    image_=''
    for p in content:
        if p["id"]==num:
            head=p["title"]
            subhead=p["subtitle"]
            image_=f"background-image: url('../static/assets/img/post{num}.jpg')"
            break
        else:
            continue
    return render_template("post.html",post_num=num,posts=content,heading=head,subheading=subhead,image=image_)



if __name__ == "__main__":
    app.run(debug=True)
