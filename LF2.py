import json
import boto3
from requests_aws4auth import AWS4Auth
import random
from opensearchpy import OpenSearch, RequestsHttpConnection

access_key = ''
secret_access_key = ''

def lambda_handler(event, context):
    
    #get message from sqs
    sqs = boto3.resource('sqs', region_name='us-east-1', aws_access_key_id=access_key, aws_secret_access_key=secret_access_key)
    
    #receive message
    queue = sqs.get_queue_by_name(
        QueueName = "Q1"
        )
    response = queue.receive_messages(MaxNumberOfMessages = 1)
    try:
        print(response[0].body)
    except:
        return
    responseVals = response[0].body.split(',')
    city = responseVals[0]
    cuisine = responseVals[1]
    numOfPPL = responseVals[2]
    date = responseVals[3]
    time = responseVals[4]
    mail = responseVals[5]

    response[0].delete()
    
    #get query from opensearch
    host = 'search-restaurant-6f75t63ixiplqxax2mocvzpxxy.us-east-1.es.amazonaws.com' # For example, my-test-domain.us-east-1.es.amazonaws.com
    region = 'us-east-1' # e.g. us-west-1
    
    session = boto3.Session(
        aws_access_key_id=access_key,
        aws_secret_access_key=secret_access_key,
    )
    
    service = 'es'
    credentials = boto3.Session().get_credentials()
    awsauth = AWS4Auth(access_key, secret_access_key, region, service)
    
    search = OpenSearch(
        hosts = [{'host': host, 'port': 443}],
        http_auth = awsauth,
        use_ssl = True,
        verify_certs = True,
        connection_class = RequestsHttpConnection
    )
    
    
    #its dying here
    query = search.search(q=cuisine, size=2000)
    arrOfHits = query['hits']['hits']
    #choose a random one from this array (do this 3 times)
    S = set()
    while len(S) != 3:
        rand_rest = random.choice(arrOfHits)
        rest_id = rand_rest['_source']['id']
        S.add(rest_id)

    rest_data = []
    #search the id in dynamodb
    for i in S:
        client2 = boto3.client('dynamodb', region_name='us-east-1', aws_access_key_id=access_key, aws_secret_access_key=secret_access_key)
        full_rest_data = client2.get_item(
            TableName = 'yelp_restaurants',
            Key = {'id': {'S': i}}
            )
        rest_data.append(full_rest_data)
    
    
    #for loop to parse data
    parsed_data = []
    for i in rest_data:
        location = i['Item']['location']['M']['display_address']['L']
        loc = ''
        for l in location:
            loc += l['S']
            loc += " "
        name = i['Item']['name']['S']

        str =  name + ", located at " + loc
        parsed_data.append(str)



    sendstr = 'Hello! Here are my ' + cuisine + " restaurant suggestion for " + numOfPPL + " people, for " + date + " at " + time + ": 1. " + parsed_data[0] + ", 2. " + parsed_data[1] + ", 3. " + parsed_data[2] + ". Enjoy your meal!"
    print(sendstr)

    client = boto3.client('ses', region_name='us-east-1', aws_access_key_id=access_key, aws_secret_access_key=secret_access_key)
    client.send_email(
        Source = 'jl11517@nyu.edu',
        Destination = {
            'ToAddresses': [mail]
        },
        Message={
            'Subject': {
                'Data': 'Food recommendation service bot'
            },
            "Body": {
                'Text':{
                    'Data': sendstr
                }
                
            }
        }

    )
    print("completed the send")

    return {
        'statusCode': 200,
        'body': json.dumps('Hello from Lambda!')
    }

