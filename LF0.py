import json
import boto3

def lambda_handler(event, context):
    messages = event['messages'][0]['unstructured']['text']
    client = boto3.client('lexv2-runtime', region_name='us-east-1', aws_access_key_id='', aws_secret_access_key='')
    botName = "FoodRecommenderBot"
    AliasName = "TSTALIASID"
    botId = "HYRFRJXCF8"
    localeId = "en_US"
    sessionId = 'user'
    inputText = messages
    
    response = client.recognize_text(botId = botId, botAliasId = AliasName, localeId = localeId, sessionId = sessionId, text = inputText)
    reply = response['messages'][0]['content']
    return {
        'statusCode': 200,
        'headers': {
            'Access-Control-Allow-Headers': 'Content-Type',
            'Access-Control-Allow-Origin': '*',
            'Access-Control-Allow-Methods': 'OPTIONS,POST,GET'
        },
        'body': reply,
    }
