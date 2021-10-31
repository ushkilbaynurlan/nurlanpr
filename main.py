from flask import Flask, render_template, request
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)

ENV = 'dev'

if ENV == 'dev':
    app.debug = True
    app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://nurlan:axTls7gisNguhbdP@postgresql-do-user-10012033-0.b.db.ondigitalocean.com:25060/nurlandb'
else:
    app.debug = False
    app.config['SQLALCHEMY_DATABASE_URI'] = ''

app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)


class Nurlan(db.Model):
    __tablename__ = 'tirkeu'
    id = db.Column(db.Integer, primary_key=True)
    IIN = db.Column(db.Integer, unique=True)
    aty = db.Column(db.String(40))
    familiya = db.Column(db.String(40))
    region = db.Column(db.String(30))
    oplata = db.Column(db.String(15))
    mamandyk = db.Column(db.String(40))
    comment = db.Column(db.Text())

    def __init__(self, IIN, aty, familiya, region, oplata, mamandyk, comment):
        self.IIN = IIN
        self.aty = aty
        self.familiya = familiya
        self.region = region
        self.oplata = oplata
        self.mamandyk = mamandyk
        self.comment = comment

        @app.route('/')
        def index():
            return render_template('index.html')

        @app.route('/submit', methods=['POST'])
        def submit():
            if request.method == 'POST':
                IIN = request.form['IIN']
                aty = request.form['aty']
                familiya = request.form['familiya']
                region = request.form['region']
                oplata = request.form['oplata']
                mamandyk = request.form['mamandyk']
                comment = request.form['comment']

                if IIN == '' or familiya == '':
                    return render_template('index.html', message='Форманы дұрыс толтырыңыз!')
                if db.session.query(Nurlan).filter(Nurlan.IIN == IIN).count() == 0:
                    data = Nurlan(IIN, aty, familiya, region, oplata, mamandyk, comment)
                    db.session.add(data)
                    db.session.commit()
                    return render_template('success.html')
                return render_template('index.html', message='Сіз бұрын тіркелгенсіз!')

        if __name__ == "__main__":
            app.run(host='0.0.0.0')
