import datetime


class Triage(object):

    uri = '/triage'

    def get(self):
        user = __user__.query.filter_by(triage=True).first()
        return __flask__.jsonify({
            'triage': user.name,
            'date': user.date.strftime('%A, %B %d, %Y')
        })

    def put(self):
        users = __user__.query.order_by(__user__.order).all()
        nextuser = False
        for user in users:
            if user.triage is True:
                user.triage = False
                __db__.session.commit()
                nextuser = True
            elif user.enabled == 0:
                continue
            elif nextuser is True:
                user.triage = True
                user.date = datetime.datetime.now()
                __db__.session.commit()
                nextuser = False
                ret = {'nexttriage': user.name, 'date': user.date.strftime('%A, %B %d, %Y')}
                break
        if nextuser is True:
            for user in users:
                if user.enabled == 1:
                    user.triage = True
                    user.date = datetime.datetime.now()
                    __db__.session.commit()
                    ret = {'nexttriage': user.name, 'date': user.date.strftime('%A, %B %d, %Y')}
                    break
        return __flask__.jsonify(ret)

