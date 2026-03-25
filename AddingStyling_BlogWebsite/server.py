from flask import Flask,render_template
import requests

app=Flask(__name__)
JSON_BIN_ENDPOINT="https://api.npoint.io/691d0e7aa29fd76f3ef5"

response=requests.get(JSON_BIN_ENDPOINT)
print(response.status_code)
content = response.json()

@app.route('/')
def homepage():
    return render_template("index.html",heading="Anime Insight",subheading="Exploring stories, characters, and emotions beyond the screen",
                           image="background-image: url('../static/assets/img/home-bg.jpg",posts=content)

@app.route('/about')
def about():
    return render_template("about.html",heading="About Me",subheading="This is what I do",
                           image="background-image: url('../static/assets/img/about-bg.jpg")

@app.route('/contact')
def contact():
    return render_template("contact.html",heading="Contact Me",subheading="Have questions? I have answers",
                           image="background-image: url('../static/assets/img/contact-bg.jpg")

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
