# coding=utf-8
from ext import db
from datetime import datetime


class USER(db.Model):
    __tablename__ = 'user'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), unique=True)
    password = db.Column(db.String(100))

    def __init__(self, name, password):
        self.name = name
        self.password = password

    @classmethod
    def check_login(cls, user, passwd):
        user = cls.query.filter_by(name=user).first()
        if user:
            if passwd == user.password:
                return {'msg': 'ok'}
            else:
                return {'msg': 'passwd error'}
        else:
            return {'msg': 'not found user'}

    @classmethod
    def resgiter(cls, user, passwd):
        msg = cls.check_login(user, passwd)
        if msg['msg'] != 'not found user':
            return 'resgitered'
        else:
            new_user = cls(name=user, password=passwd)
            return new_user

    def __repr__(self):
        return '<user:%s>' % self.name


class TODO(db.Model):
    __tablename__ = 'todo'
    id = db.Column(db.Integer, primary_key=True)
    user = db.Column(db.String(100))
    todo = db.Column(db.String(100), unique=True)
    created = db.Column(db.DateTime, default=datetime.now())
    description = db.Column(db.String(200))

    def __init__(self, user, todo, description, created=datetime.now()):
        self.user = user
        self.todo = todo
        self.created = created
        self.description = description

    @classmethod
    def get_todo(cls, user):
        todos = cls.query.filter_by(user=user)
        todo_list = []
        for each in todos:
            todo_dict = {}
            todo_dict['id'] = each.id
            todo_dict['todo'] = each.todo
            todo_dict['created'] = each.created
            todo_dict['description'] = each.description
            todo_list.append(todo_dict)
        return todo_list


    def __repr__(self):
        return '<todo:%s>' % self.todo
