import requests
import json

print 'Testing Python File!'

data = {
        "id": "Postman Testing",
        "method": "down.query_data",
        "params": {
                "limit":1,
                "order_by":"id",
                "direction":"DESC"
        }
    }

r = requests.post('http://127.0.0.1:8000/api', json.dumps(data))
json.loads(r.text)

exit(0)
