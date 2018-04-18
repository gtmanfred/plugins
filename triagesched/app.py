# -*- coding: utf-8 -*-

# Import Python Libraries
import importlib.util
import os

import flask
import flask_restful

load_objects = (
    flask,
    flask_restful,
)

def _load_module(name, path):
    spec = importlib.util.spec_from_file_location(name, path)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    for obj in load_objects:
        setattr(module, obj.__name__, obj)
    return module

def setup_app():
    app = flask.Flask(__name__)
    with os.scandir('.') as rit:
        for entry in rit:
            if not entry.name.startswith('.') and entry.is_dir():
                modname = entry.path[2:]
                modapp = _load_module(modname, f'{modname}/app.py')
                app.register_blueprint(modapp.create_app())
    return app
