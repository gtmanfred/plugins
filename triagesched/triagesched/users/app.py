class User(object):

    uri = '/users/<string:userid>'

    def get(self, userid):
        user = __user__.query.get(userid)
        if not user:
            return {'Error': f'Unable to find user: {userid}'}, 404
        return __flask__.jsonify({'user': __to_dict__(user)})

    def put(self, userid):
        user = __user__.query.get(userid)
        if not user:
            return {'Error': f'Unable to find user: {userid}'}, 404
        for key, value in __flask__.request.json.items():
            if key in ('userid', 'date'):
                continue
            setattr(user, key, value)
        __db__.session.commit()
        return __flask__.jsonify({'user': __to_dict__(user)})

    def delete(self, userid):
        user = __user__.query.get(userid)
        if not user:
            return {'Error': f'Unable to find user: {userid}'}, 404
        __db__.session.delete(user)
        __db__.session.commit()
        if __user__.query.get(userid):
            return {'Error': 'Failed to delete: {userid}'}, 500
        return __flask__.jsonify({'message': 'success'})


class Users(object):

    uri = '/users'

    def get(self):
        if 'enabled' in __flask__.request.args:
            users = __user__.query.filter_by(enabled=True).all()
        else:
            users = __user__.query.all()
        if not users:
            return {'Error': 'No users defined'}, 404
        return __flask__.jsonify({'users': [__to_dict__(user) for user in users]})

    def post(self):
        name, order = __flask__.request.json['name'], __flask__.request.json['order']
        user = __user__(name=name, order=order)
        __db__.session.add(user)
        __db__.session.commit()
        return __flask__.jsonify(__to_dict__(user))
