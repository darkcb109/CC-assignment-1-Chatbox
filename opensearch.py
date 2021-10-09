from bs4 import BeautifulSoup
from opensearchpy import OpenSearch, RequestsHttpConnection
from requests_aws4auth import AWS4Auth
import boto3
import glob
import json

bulk_file = ''
id = 1

# This loop iterates through all HTML files in the current directory and
# indexes two things: the contents of the first h1 tag and all other text.
files = ['dataI.json']



for html_file in files:

    with open(html_file) as json_file:
        restaurant_list = json.load(json_file)
    for restaurants in restaurant_list:
        #get id and cuisine with restaurants
        rest_id = restaurants['id']
        categories = restaurants['categories']
        cuisines = []
        for cuisine in categories:
            alias = cuisine['alias']
            if alias == "ramen":
                alias = "japanese"
            elif alias == 'shanghainese':
                alias = "chinese"
            elif alias == 'szechuan':
                alias = "chinese"
            elif alias == 'cantonese':
                alias = "chinese"
            elif alias == 'dimsum':
                alias = "chinese"
            elif alias == 'taiwanese':
                alias = "chinese"
            elif alias == 'indpak':
                alias = 'indian'
            cuisines.append(alias)
        index = { 'id': rest_id, 'cuisine': cuisines}
        # If running this script on a website, you probably need to prepend the URL and path to html_file.

        # The action_and_metadata portion of the bulk file
        bulk_file += '{ "index" : { "_index" : "restaurant", "_type" : "_doc", "_id" : "' + str(id) + '" } }\n'

        # The optional_document portion of the bulk file
        bulk_file += json.dumps(index) + '\n'

        id += 1

host = 'search-restaurant-6f75t63ixiplqxax2mocvzpxxy.us-east-1.es.amazonaws.com' # For example, my-test-domain.us-east-1.es.amazonaws.com
region = 'us-east-1' # e.g. us-west-1

session = boto3.Session(
    aws_access_key_id='AKIAXY4BPPZV2XWERI75',
    aws_secret_access_key='5vvFMgDmsj0uXLKzHXb/ZimtHSul5JHxi/YZPfyR',
)

service = 'es'
credentials = boto3.Session().get_credentials()
awsauth = AWS4Auth(credentials.access_key, credentials.secret_key, region, service)

search = OpenSearch(
    hosts = [{'host': host, 'port': 443}],
    http_auth = awsauth,
    use_ssl = True,
    verify_certs = True,
    connection_class = RequestsHttpConnection
)

search.bulk(bulk_file)

print(search.search(q='chinese'))


'''
for i in range(1, 2265):
    response = search.delete(
        index = 'restaurant',
        id = i
    )
'''