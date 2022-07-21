import requests
from datetime import datetime
from lib.mongo import *


client = get_connection()
db = client['youla']
parser_collection = db['parsed']
