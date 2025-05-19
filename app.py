from flask import Flask, render_template, request
from flask_sqlalchemy import SQLAlchemy
from werkzeug.utils import redirect

app=Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///site.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False  # Отключаем предупреждения

db = SQLAlchemy(app)


class Post(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(300), nullable=False)
    text = db.Column(db.Text, nullable=False)

#декоратор
@app.route("/index")
@app.route("/") #ссылка
def index():
    return render_template('index.html')

@app.route("/recipes")
def recipes():
    recipes = Post.query.all()
    return render_template('recipes.html', recipes=recipes)

@app.route("/create", methods=['POST','GET'])
def create():
    if request.method == 'POST':
        title = request.form['title']
        text = request.form['text']

        post=Post(title=title, text=text)

        try:
            db.session.add(post)
            db.session.commit()
            return redirect('/')
        except:
            return 'При добавлении произошла ошибка!'
    else:
        return render_template('create.html')


if __name__=='__main__': #если запускает только через это файл
     app.run(debug=True)  #обновление

