class Users(object):

    uri = '/users'

    def get(self):
        return flask.jsonify({'hello': 'world'})
