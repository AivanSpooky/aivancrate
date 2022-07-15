from this import d
from flask import Flask, redirect, render_template, url_for, request, redirect
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = 'sqlite:///top.db'
db_top = SQLAlchemy(app)

app.config["SQLALCHEMY_DATABASE_URI"] = 'sqlite:///aivanextremes.db'
db_ex = SQLAlchemy(app)

app.config["SQLALCHEMY_DATABASE_URI"] = 'sqlite:///aivanelevels.db'
db_l = SQLAlchemy(app)



class Article(db_ex.Model):
    id = db_ex.Column(db_ex.Integer, primary_key=True)
    level_name = db_ex.Column(db_ex.String, nullable=True)
    creator_name = db_ex.Column(db_ex.String, nullable=True)
    img = db_ex.Column(db_ex.String, nullable=True)

    attempts = db_ex.Column(db_ex.String, nullable=True)
    device = db_ex.Column(db_ex.String, nullable=True)
    fps = db_ex.Column(db_ex.String, nullable=True)
    opinion = db_ex.Column(db_ex.Text, nullable=True)
    difficulty = db_ex.Column(db_ex.Integer, nullable=True)

    def __repr__(self):
        return '<Article %r>' % self.id


class Article_l(db_l.Model):
    id = db_l.Column(db_l.Integer, primary_key=True)
    level_name = db_l.Column(db_l.String, nullable=True)
    creator_name = db_l.Column(db_l.String, nullable=True)
    img = db_l.Column(db_l.String, nullable=True)
    difficulty = db_l.Column(db_l.Integer, nullable=True)
    state = db_l.Column(db_l.String, nullable=True)

    def __repr__(self):
        return '<Article_l %r>' % self.id


class Article_top(db_top.Model):
    id = db_top.Column(db_top.Integer, primary_key=True)
    nickname = db_top.Column(db_top.String, nullable=True)

    top5_diff = db_top.Column(db_top.String, nullable=True)
    top5_text = db_top.Column(db_top.String, nullable=True)
    top4_diff = db_top.Column(db_top.String, nullable=True)
    top4_text = db_top.Column(db_top.String, nullable=True)
    top3_diff = db_top.Column(db_top.String, nullable=True)
    top3_text = db_top.Column(db_top.String, nullable=True)
    top2_diff = db_top.Column(db_top.String, nullable=True)
    top2_text = db_top.Column(db_top.String, nullable=True)
    top1_diff = db_top.Column(db_top.String, nullable=True)
    top1_text = db_top.Column(db_top.String, nullable=True)

    version = db_top.Column(db_top.String, nullable=True)
    icon = db_top.Column(db_top.String, nullable=True)

    def __repr__(self):
        return '<Article_top %r>' % self.id


@app.route('/')
def index():
    return render_template("main.html")

@app.route('/pass', methods=['POST', 'GET'])
def passw():
    if request.method == "POST":
        passwo = request.form['passwo']
        if passwo == "95877":
            return redirect('/ax')
        else:
            return render_template("cr_pass.html", notpas=True)
    else:
        return render_template("cr_pass.html", notpas=False)

@app.route('/aboutaivan')
def aboutaivan():
    return render_template("aboutaivan.html")

@app.route('/rules')
def rules():
    return render_template("rules.html")

@app.route('/ax', methods=['POST', 'GET'])
def create_ax():
    if request.method == "POST":
        level_name = request.form['level_name']
        creator_name = request.form['creator_name']
        img = request.form['img']

        attempts = request.form['attempts']
        device = request.form['device']
        fps = request.form['fps']
        opinion = request.form['opinion']

        difficulty = request.form['difficulty']

        article = Article(level_name=level_name, creator_name=creator_name, img=img, attempts=attempts, device=device, fps=fps, opinion=opinion, difficulty=difficulty)

        try:
            db_ex.session.add(article)
            db_ex.session.commit()
            return redirect('/')
        except:
            return 'Ошибка заполнения данных'


    else:
        return render_template("create_ax.html")


@app.route('/aivanextremes')
def extremes():
    app.config["SQLALCHEMY_DATABASE_URI"] = 'sqlite:///aivanextremes.db'
    articles = Article.query.order_by(Article.difficulty).all()
    return render_template("aivanextremes.html", articles=articles)

@app.route('/aivanlevels')
def levels():
    app.config["SQLALCHEMY_DATABASE_URI"] = 'sqlite:///aivanlevels.db'
    articles = Article_l.query.order_by(Article_l.id).all()
    return render_template("aivanlevels.html", articles=articles)

@app.route('/top')
def top():
    app.config["SQLALCHEMY_DATABASE_URI"] = 'sqlite:///top.db'
    articles = Article_top.query.order_by(Article_top.id).all()
    return render_template("top.html", articles=articles)


if __name__ == "__main__":
    app.run(debug=False,host='0.0.0.0')
