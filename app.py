# coding:utf-8
import os
from flask import Flask, render_template, session, request, jsonify, redirect, url_for
from flask_script import Manager, Shell
from flask_migrate import Migrate, MigrateCommand
from flask_sqlalchemy import SQLAlchemy


app = Flask(__name__)
db = SQLAlchemy(app)
manager = Manager(app)
migrate = Migrate(app, db)

basedir = os.path.abspath(os.path.join(__file__))

app.config['SQLALCHEMY_DATABASE_URI'] = "mysql://{username}:{password}@{server}/{db}".format(username='root',
                                                                                             password='050400',
                                                                                             server='localhost',
                                                                                             db='haha')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True
app.secret_key='djaildhjsdfhjsofjilsfjsfjpjfojgogj'


class USER(db.Model):
    __tablename__ = 'user'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), unique=True)
    password = db.Column(db.String(100))

    def __repr__(self):
        return '<user:%s>' %self.name


def make_shell_context():
    return dict(app=app, db=db, USER=USER)


manager.add_command("shell", Shell(make_context=make_shell_context))
manager.add_command("db", MigrateCommand)


@app.route('/')
def index():
    user = session.get('user', '')
    return render_template('index.html', user=user)


@app.route('/login', methods=['GET'])
def login():
    return render_template('login.html')


@app.route('/resgiter', methods=['GET'])
def resgiter():
    return render_template('resgiter.html')


@app.route('/login_out', methods=['GET'])
def login_out():
    session['user'] = None
    return redirect(url_for('index'))


@app.route('/check_login', methods=['POST'])
def check_login():
    if request.method == 'POST':
        user = request.form['user']
        password = request.form['password']
        data = {'code': 1, 'msg': ''}
        user_obj = USER.query.filter_by(name=user).first()
        if user_obj:
            if password == user_obj.password:
                data['code'] = 0
                data['msg'] = 'ok'
                session['user'] = user
            else:
                data['msg'] = 'password error!'
        else:
            data['msg'] = 'not found user!'

        return jsonify(data)
    return redirect(url_for('login'))


@app.route('/check_resgiter', methods=['POST'])
def check_resgiter():
    if request.method == 'POST':
        user = request.form['user']
        password = request.form['password']
        data = {'code': 1, 'msg': ''}
        if user and password:
            if USER.query.filter_by(name=user).first():
                data['msg'] = 'you already resgitered!'
            else:
                new_user = USER(name=user, password=password)
                db.session.add(new_user)
                db.session.commit()
                data['code'] = 0
                data['msg'] = 'ok'
        else:
            data['msg'] = 'user or password is empty!'

        return jsonify(data)
    return redirect(url_for('resgiter'))


@app.errorhandler(404)
def not_found(e):
    return render_template('404.html'), 404


@app.errorhandler(405)
def method_not_allow(e):
    return render_template('405.html'), 405



if __name__ == '__main__':
    manager.run()
