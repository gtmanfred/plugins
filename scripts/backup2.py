import hub.struct

this = hub.struct.Hub()

this.tools.pack.add('aio', pypath='hub.mods.aio')
this.tools.pack.add('triagedb', pypath='triagesched.mods.triagedb')

this.tools.loop.start(this.triagedb.db.setupdb, 'sqlite:///data.db')

this.aio.http.web(
    {'triageapp': 'triagesched.mods.triageapp'},
    prefix='/api/v1',
    static='/Users/daniel/github/plugins/triagesched/triagesched/html',
    staticpath='/html/',
)
