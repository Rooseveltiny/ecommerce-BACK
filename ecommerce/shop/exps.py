
import json


some_dict = [{
    'kek': 'kek',
    'lol': 'some_lol',
    'array': ['kek', 'lol', 'qq']
}]
arr = ['kek', 'lol', 'cheburek', some_dict]


print(json.dumps(arr))