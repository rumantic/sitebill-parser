import requests
from datetime import datetime
from lib.mongo import *


client = get_connection()
db = client['youla']
parser_collection = db['parsed']

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
                "latitude": None,
                "longitude": None,
                "city": "576d061ad53f3d80945f9928",
                "distanceMax": None
            },
            "search": "",
            "cursor": ""
        },
        "extensions": {
            "persistedQuery": {
                "version": 1,
                "sha256Hash": ""+sha256Hash+""
            }
        }
    }
    return data

for page in range(1,2):
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

