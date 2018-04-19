# -*- coding: utf-8 -*-

__version__ = 1


class Users(object):

    uri = '/users'

    def get(self):
        return __flask__.jsonify({'hello': 'world'})
