# -*- coding: utf-8 -*-

from datetime import datetime
from . import db


class Category(db.Model):
    __tablename__ = 'categories'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(64), unique=True)

    def __repr__(self):
        return "<Category %r>" % self.name


class Snippet(db.Model):
    __tablename__ = 'snippets'
    id = db.Column(db.Integer, primary_key=True)
    summary = db.Column(db.Text)
    keywords = db.Column(db.Text)
    body = db.Column(db.Text)
    body_html = db.Column(db.Text)
    category = db.Column(db.Integer, db.ForeignKey('categories.id'))
    timestamp = db.Column(db.DateTime, index=True, default=datetime.utcnow)
    update_timestamp = db.Column(db.DateTime, index=True, default=datetime.utcnow)

    def __repr__(self):
        return "<Snippet %r>" % self.id


