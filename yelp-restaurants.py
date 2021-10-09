import requests
import json

locations = ['east harlem', 'west Harlem', 'Midtown', 'soho manhattan',  'lower east side', 'upper east side', 'east village', 'tribeca', 'chelsea', 'flatiron']

def get_businesses(location, term, api_key):
    headers = {'Authorization': 'Bearer %s' % api_key}
    url = 'https://api.yelp.com/v3/businesses/search'

    data = []
    for offset in range(0, 800, 50):
        for loc in location:
            params = {
                'limit': 50, 
                'radius': 1500,
                'location': loc.replace(' ', '+'),
                'categories': term.replace(' ', '+'),
                'term': "restaurants",
                'offset': offset,
                'radius': 10000
            }

            response = requests.get(url, headers=headers, params=params)
            if response.status_code == 200:
                data += response.json()['businesses']
            elif response.status_code == 400:
                print('400 Bad Request')
                break

    return data

all_data = {}


api_key = "zsaoselEJUzjKsUbyG5on3PZYL13Acz6nTrhP0LbJdDwOqmERZhckhObEK3U9P80K9obIcY8ZW6cgK1XOJvaQxrIm1_aWh9kHNtMwGAGFuKebNdN_EHzOPte7rBbYXYx"



term = "japanese"
data = get_businesses(locations, term, api_key)
for i in data:
    all_data[i['id']] = i
print("done with japanese restaurants")

term = 'mexican'
data = get_businesses(locations, term, api_key)
for i in data:
    all_data[i['id']] = i
print("done with mexican restaurants")

term = 'indian'
data = get_businesses(locations, term, api_key)
for i in data:
    all_data[i['id']] = i
print("done with indian restaurants")


term = 'chinese'
data = get_businesses(locations, term, api_key)
for i in data:
    all_data[i['id']] = i
print("done with chinese restaurants")

term = 'thai'
data = get_businesses(locations, term, api_key)
for i in data:
    all_data[i['id']] = i
print("done with thai restaurants")

print("completed scraping")


outVal = []

for i in all_data:
    outVal.append(all_data[i])
with open('data.json', 'w') as outfile:
    outfile.write(json.dumps(outVal))
outfile.close()

counts = 0

import boto3
from decimal import Decimal
def load_data(data):
    global counts
    dynamodb = boto3.resource('dynamodb', region_name='us-east-1', aws_access_key_id='AKIAXY4BPPZV2XWERI75', aws_secret_access_key='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')
    table = dynamodb.Table('yelp_restaurants')
    for restaurants in data:
        counts = counts + 1
        table.put_item(Item=restaurants)


with open("data.json") as json_file:
    restaurant_list = json.load(json_file, parse_float=Decimal)
load_data(restaurant_list)


print('completed with ' + str(counts) + ' restaurants put into databse')
