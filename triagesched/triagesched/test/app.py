# -*- coding: utf-8 -*-
__version__ = 1


class Test(object):

    uri = '/test'

    def get(self):
        return __flask__.jsonify({'hello': 'world'})

    def post(self):
        return __flask__.jsonify({'test post': 'success!'})
