import json
import datetime
import boto3

def lambda_handler(event, context):
    #entity = event["intent"]["slots"]["Name"].title()
    intent = event['interpretations'][0]["intent"]["name"]
    value = event["inputTranscript"]
    content = ""
    confirmationState = None
    state = 'InProgress'
    types = "ConfirmIntent"
    
    city = ''
    cusine = ''
    numOfPeople = 0
    date = ''
    time = ''
    phone = ''
    

    
    if intent == "DiningSuggestionsIntent":
        try:
            city = eventintent = event['interpretations'][0]["intent"]["slots"]['city']['value']['interpretedValue']
            cusine = eventintent = event['interpretations'][0]["intent"]["slots"]['cusine']['value']['interpretedValue']
            numOfPeople = eventintent = event['interpretations'][0]["intent"]["slots"]['numOfPeople']['value']['interpretedValue']
            date = eventintent = event['interpretations'][0]["intent"]["slots"]['date']['value']['interpretedValue']
            time = eventintent = event['interpretations'][0]["intent"]["slots"]['time']['value']['interpretedValue']
            phone = eventintent = event['interpretations'][0]["intent"]["slots"]['phone']['value']['originalValue']
            content = "You’re all set. Expect my suggestions shortly! Have a good day."
            state = 'Fulfilled'
            types = "Close"
            
            
            #integrate sqs
            
            sendUrl = "https://sqs.us-east-1.amazonaws.com/534458105451/Q1"
            #sendString = city + "\t" + cusine + "\t" + numOfPeople + "\t" + date + "\t" + time + "\t" + phone
            sendBody = city + "," + cusine + "," + numOfPeople + "," + date + "," + time + "," + phone
            
            #do the method
            client = boto3.client('sqs', region_name='us-east-1', aws_access_key_id='AKIAXY4BPPZV2XWERI75', aws_secret_access_key='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')
            result = client.send_message(
                QueueUrl=sendUrl,
                MessageBody=sendBody
                )
            
            response =  {
                "sessionState": {
                    
                    "dialogAction":
                    {
                        "type":types,
                     },
                     "intent": {
                        "confirmationState": confirmationState,
                        "name": intent,
                        "slots": {},
                     "state": state
                    }
                    
                },
                "messages":
                        [{
                             "contentType":"PlainText",
                             #"content": "The intent you are in now is "+intent+"! and the context is: " + str(event)
                             "content": content
                        }]  
                    }
        except:
            city = eventintent = event['interpretations'][0]["intent"]["slots"]['city']
            cusine = eventintent = event['interpretations'][0]["intent"]["slots"]['cusine']
            numOfPeople = eventintent = event['interpretations'][0]["intent"]["slots"]['numOfPeople']
            date = eventintent = event['interpretations'][0]["intent"]["slots"]['date']
            time = eventintent = event['interpretations'][0]["intent"]["slots"]['time']
            phone = eventintent = event['interpretations'][0]["intent"]["slots"]['phone']
            if city == None:
                slots = 'city'
            elif cusine == None:
                slots = 'cusine'
            elif numOfPeople == None:
                slots = 'numOfPeople'
            elif date == None:
                slots = 'date'
            elif time == None:
                slots = 'time'
            elif phone == None:
                slots = 'phone'
            else:
                slots = ""
            types = 'ElicitSlot'
            
            if city != None:
                cityVal = city['value']['interpretedValue']
                if cityVal.lower() != 'manhattan' and cityVal.lower() != 'nyc' and cityVal.lower() != 'new york city':
                    slots = 'city'
                    response =  {
                        "sessionState": {
                            
                            "dialogAction":
                            {
                                'slotToElicit': slots,
                                "type":types
                             },
                             "intent": {
                                "confirmationState": confirmationState,
                                "name": intent,
                                "slots": event['interpretations'][0]["intent"]["slots"],
                             "state": state
                            }
                            
                        },
                        "messages":
                        [{
                             "contentType":"PlainText",
                             "content": "I'm sorry, we only support manhattan/NYC right now"
                        }]  
                    }
                    return response
            
            today = datetime.date.today()
            cuisineTypes = ['indian', 'mexican', 'japanese','chinese', 'thai']
            cuisineBit = True
            pplBit = True
            dateBit = True
            timeBit = True
            mailBit = True
            
            if cusine != None:
                if cusine['value']['interpretedValue'] not in cuisineTypes:
                    slots = "cusine"
                    response =  {
                        "sessionState": {
                            
                            "dialogAction":
                            {
                                'slotToElicit': slots,
                                "type":types
                             },
                             "intent": {
                                "confirmationState": confirmationState,
                                "name": intent,
                                "slots": event['interpretations'][0]["intent"]["slots"],
                             "state": state
                            }
                            
                        },
                        "messages":
                        [{
                             "contentType":"PlainText",
                             "content": "I'm sorry, we only have japanese, chinese, indian, mexican, and thai right now"
                        }]  
                    }
                    return response
                    
            if numOfPeople != None:
                if 0 >= int(numOfPeople['value']['interpretedValue']) or int(numOfPeople['value']['interpretedValue']) >= 20:
                    pplBit = False
            if date != None:
                currDate = date['value']['interpretedValue'].split('-')
                dates = datetime.date(int(currDate[0]), int(currDate[1]), int(currDate[2]))
                if today > dates:
                    dateBit = False
            if time != None:
                currDate = date['value']['interpretedValue'].split('-')
                dates = datetime.date(int(currDate[0]), int(currDate[1]), int(currDate[2]))
                fakeTime = time['value']['interpretedValue'].split(':')
                current_time =  (datetime.datetime.now().hour*60) + datetime.datetime.now().minute
                currMins = (int(fakeTime[0])  * 60) + int(fakeTime[1])
                if dates == today and currMins < current_time:
                    timeBit = False
            if phone != None:
                Email = phone['value']['interpretedValue'].split('-')
                if '@' not in Email:
                    mailBit = False
            

            if not pplBit:
                slots = 'numOfPeople'
                pplBit = True
            elif not dateBit:
                slots = 'date'
                dateBit = True
            elif not timeBit:
                slots = 'time'
                timeBit = True
            elif not mailBit:
                slots = 'phone'
                mailBit = True
                    
            response =  {
                "sessionState": {
                    
                    "dialogAction":
                    {
                        'slotToElicit': slots,
                        "type":types
                     },
                     "intent": {
                        "confirmationState": confirmationState,
                        "name": intent,
                        "slots": event['interpretations'][0]["intent"]["slots"],
                     "state": state
                    }
                    
                }
                    }
            
            

    
    
    
                
    return response