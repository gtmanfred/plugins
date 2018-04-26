# -*- coding: utf-8 -*-
import datetime
import sqlalchemy
import sqlalchemy_aio
import sqlalchemy.schema


async def setupdb(hub, dburi, debug=False):
    engine = sqlalchemy.create_engine(dburi, strategy=sqlalchemy_aio.ASYNCIO_STRATEGY)

    metadata = sqlalchemy.MetaData(engine)

    hub.triagedb._users = sqlalchemy.Table(
        'users', metadata,
        sqlalchemy.Column('userid', sqlalchemy.Integer, primary_key=True, autoincrement=True),
        sqlalchemy.Column('name', sqlalchemy.Text, nullable=False),
        sqlalchemy.Column('order', sqlalchemy.Integer, unique=True),
        sqlalchemy.Column('triage', sqlalchemy.Boolean, nullable=False, default=False),
        sqlalchemy.Column('enabled', sqlalchemy.Boolean, nullable=False, default=True),
        sqlalchemy.Column('date', sqlalchemy.DateTime, default=datetime.datetime.utcnow),
    )

    test = await engine.has_table('users')
    if not test:
        await engine.execute(sqlalchemy.schema.CreateTable(hub.triagedb._users))
    hub.triagedb._conn = await engine.connect()


def to_dict(hub, user):
    return {
        'userid': user.userid,
        'name': user.name,
        'order': user.order,
        'triage': user.triage,
        'enabled': user.enabled,
        'date': user.date.strftime('%A, %B %d, %Y'),
    }
