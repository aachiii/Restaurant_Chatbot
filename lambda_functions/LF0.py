import json
import boto3

client = boto3.client('lex-runtime')


def lambda_handler(event, context):

    try:

        response = client.post_text(
            botName='ChiquChatbot',
            botAlias='chiquli',
            userId='10',
            sessionAttributes={
                },
            requestAttributes={
                
            },
            inputText = event["input"]
        )
        
    except:
        response = {"message":"you got an error"}

    return {
            'statusCode': 200,
            'body': json.dumps(response['message']) 