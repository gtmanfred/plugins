# -*- coding: utf-8 -*-

import json
import requests

for idx, user in enumerate(['daniel', 'megan', 'gareth']):
    print(requests.post('http://localhost:5000/api/v1/users',
                 data=json.dumps({'name': user, 'order': idx + 1}),
                 headers={'Content-Type': 'application/json'}).json())
