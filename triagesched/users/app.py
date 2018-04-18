import flask_restful
class Users(flask_restful.Resource):

    uri = '/users'

    def get(self):
        return flask.jsonify({'hello': 'world'})
