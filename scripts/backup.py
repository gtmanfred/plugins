import hub.struct

this = hub.struct.Hub()
this.tools.pack.add('dbs', pypath='hub.mods.dbs')
this.tools.pack.add('aio', pypath='hub.mods.aio')

uri = './triagesched/data.db'
print(this.dbs.sqlite.query('select * from users', uri=uri))
"""
uri = 'postgresql://daniel:braves123@localhost/daniel'
print(this.dbs.postgres.query('select * from users', uri=uri))
"""


print(this.tools.loop.start(this.aio.http.query, url='http://icanhazip.com'))
