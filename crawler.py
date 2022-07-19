import os
import requests
from pymongo import MongoClient
from datetime import datetime

#mongo_host = os.environ.get('MONGO_HOST', '192.168.1.37')
mongo_host = os.environ.get('MONGO_HOST', 'not_defined')
mongo_user = os.environ.get('MONGO_USER', '')
mongo_pass = os.environ.get('MONGO_PASS', '')
mongo_port = int(os.environ.get('MONGO_PORT', 27017))
if mongo_host == 'not_defined':
    print('mongo_host not defined')
    exit()

client = MongoClient(mongo_host,
                     username=mongo_user,
                     password=mongo_pass,
                     port=mongo_port)
db = client['youla']
parser_collection = db['parsed']

print(datetime.now().strftime("%Y-%m-%d %H:%M:%S"), "crawler start, mongo_host = ", mongo_host)
#print(parser_collection.find_one())
#print(datetime.now().strftime("%Y-%m-%d %H:%M:%S"), "after get next record")
#exit()

headers = {
    'x-uid': '62b420846162a'
}


def get_request_data ( page, sha256Hash ):
    data = {
        "operationName": "catalogProductsBoard",
        "variables": {
            "sort": "DATE_PUBLISHED_DESC",
            "attributes": [
                {
                    "slug": "sobstvennik_ili_agent",
                    "value": [
                        "10705"
                    ],
                    "from": None,
                    "to": None
                },
                {
                    "slug": "categories",
                    "value": [
                        "prodaja-kvartiri"
                    ],
                    "from": None,
                    "to": None
                }
            ],
            "datePublished": None,
            "location": {
                "latitude": 61.254032,
                "longitude": 73.3964,
                "city": None,
                "distanceMax": 10000
            },
            "search": "",
            "cursor": "{\"page\":"+str(page)+",\"totalProductsCount\":100}"
        },
        "extensions": {
            "persistedQuery": {
                "version": 1,
                "sha256Hash": ""+sha256Hash+""
            }
        }
    }
    return data

for page in range(1,3):
    data = get_request_data(page, "6e7275a709ca5eb1df17abfb9d5d68212ad910dd711d55446ed6fa59557e2602")
    #print(data)
    #response = data;
    response = requests.post("https://api-gw.youla.io/federation/graphql", json=data, headers=headers).json()
    for item in response['data']['feed']['items']:
        #print(item)
        item_new = item
        success = False
        try:
            item_new['_id'] = item['product']['id']
            parser_collection.insert_one(item_new)
            success = True
        except:
            success = False
            #print('Error on insert')

        if success:
            print (datetime.now().strftime("%Y-%m-%d %H:%M:%S"), "added " + item_new['_id'])

    #file = open('./json/new/response'+str(page)+'.json', 'w')
    #file.write(json.dumps(response['data']['feed']['items']))
    #file.close()
exit()

