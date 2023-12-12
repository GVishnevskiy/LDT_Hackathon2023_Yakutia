import json


d = {
    "name": "interpolator",
    "children": {
        'name': "key",
        "size": "value"
        }
    }
j = json.dumps(d, indent=4)
with open('sample.json', 'w') as f:
    print(j, file=f)