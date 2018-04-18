# -*- coding: utf-8 -*-

# Import Python Libraries
import importlib
import inspect
import os

import flask
import flask_restful

load_objects = (
    flask,
    flask_restful,
)

def _load_module(name):
    module = importlib.import_module(name)
    for obj in load_objects:
        setattr(module, obj.__name__, obj)
    return module

def create_blueprint_app(modapp):
    app = flask.Blueprint(modapp.__name__, modapp.__name__)
    api = flask_restful.Api(app)
    for obj in inspect.getmembers(modapp, inspect.isclass):
        blueprint = obj[1]
        api.add_resource(blueprint, blueprint.uri)
    return app

def setup_app():
    app = flask.Flask(__name__)
    with os.scandir('.') as rit:
        for entry in rit:
            if not entry.name.startswith('.') and entry.is_dir():
                modname = entry.path[2:]
                modapp = _load_module(f'{modname}.app')
                app.register_blueprint(create_blueprint_app(modapp))
    return app

setup_app().run()
