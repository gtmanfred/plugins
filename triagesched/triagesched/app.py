# -*- coding: utf-8 -*-

# Import Python Libraries
import importlib.util
import inspect
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
        setattr(module, f'__{obj.__name__}__', obj)
    return module


def create_resource(blueprint):
    setattr(
        blueprint,
        'methods',
        list(map(
            lambda item: next(iter(item)).upper(),
            inspect.getmembers(blueprint, inspect.isfunction)
        ))
    )
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

    with os.scandir(os.path.dirname(__file__)) as rit:
        for entry in rit:
            if entry.name[0] not in ('.', '_') and entry.is_dir():
                modfile = f'{entry.path}/app.py'
                modname = f'{os.path.basename(entry.path)}.app'
                app.register_blueprint(create_blueprint_app(_load_module(modname, modfile)))
    return app


if __name__ == '__main__':
    setup_app().run()
