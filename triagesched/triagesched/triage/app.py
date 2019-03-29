import datetime


class Triage(object):

    uri = '/triage'

    def get(self):
        user = __user__.query.filter_by(triage=True).first()
        users = __user__.query.filter_by(enabled=True).order_by(__user__.order).all()
        if not user:
            user = __user__.query.order_by(__user__.order).first()
            user.triage = True
            __db__.session.commit()
        for n, a in enumerate(users):
            if a.triage:
                if n >= len(users) - 1:
                    next_user = users[0]
                else:
                    next_user = users[n + 1]
        return __flask__.jsonify({
            'triage': user.name,
            'date': user.date.strftime('%A, %B %d, %Y'),
            'next_user': next_user.name,
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
