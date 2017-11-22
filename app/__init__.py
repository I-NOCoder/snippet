# -*- coding: utf-8 -*-

from flask import Flask
from flask_bootstrap import Bootstrap
from flask_sqlalchemy import SQLAlchemy
from flask_pagedown import PageDown
from config import config
from filters import filters

bootstrap = Bootstrap()
db = SQLAlchemy()
pagedown = PageDown()


def create_app(config_name):
    app = Flask(__name__)
    app.config.from_object(config[config_name])
    config[config_name].init_app(app)

    bootstrap.init_app(app)
    db.init_app(app)
    pagedown.init_app(app)

    from .views import main as main_blueprint
    app.register_blueprint(main_blueprint)

    for func in filters:
        app.add_template_filter(func, func.__name__)

    return app
