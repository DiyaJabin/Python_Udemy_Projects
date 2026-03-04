from flask import Flask,render_template
import requests

app = Flask(__name__)

blog_response = requests.get("https://api.npoint.io/c790b4d5cab58020d391")

@app.route('/')
def homepage():
    return render_template('index.html',posts = blog_response.json())
@app.route('/num=<int:id>')
def get_post(id):
    return render_template('post.html',id=id,posts = blog_response.json())



if __name__ == '__main__':
    app.run(debug=True)
