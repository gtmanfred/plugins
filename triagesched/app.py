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
        setattr(module, f'__{obj.__name__}__', obj)
    return module


def create_resource(blueprint):
    return type(blueprint.__name__, (blueprint, flask_restful.Resource), {})


def create_blueprint_app(modapp):
    version = getattr(modapp, '__version__', 1)
    app = flask.Blueprint(modapp.__name__, modapp.__name__)
    api = flask_restful.Api(app)
    for obj in inspect.getmembers(modapp, inspect.isclass):
        blueprint = obj[1]
        api.add_resource(create_resource(blueprint), f'/api/v{version}{blueprint.uri}')
    return app


def setup_app():
    app = flask.Flask(__name__)

    with os.scandir('.') as rit:
        for entry in rit:
            if entry.name[0] not in ('.', '_') and entry.is_dir():
                modname = f'{entry.path[2:]}.app'
                app.register_blueprint(create_blueprint_app(_load_module(modname)))
    return app


if __name__ == '__main__':
    setup_app().run()
