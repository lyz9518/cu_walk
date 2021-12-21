import json
import boto3


def email_from_token(event):
    # get user email from token, email is primary key in DB
    access_token = event['queryStringParameters']['accessToken']
    client = boto3.client('cognito-idp')
    response = client.get_user(
        AccessToken=access_token
    )
    email = ""
    for d in response['UserAttributes']:
        if d['Name'] == 'email':
            email = d['Value']
    user_info = {
        'Username': response['Username'],
        'Email': email
    }
    print(user_info)
    return user_info['Email']


def get_contact(email):
    client = boto3.client('dynamodb')
    response = client.get_item(
        TableName='user_profile',
        Key={
            'email': {
                'S': email
            }
        }
    )
    raw = response['Item']
    print(raw)
    return raw['emergency_contact']['N']

def send_SMS(contact):
    sns_client = boto3.client("sns")
    phone_num = "+1" + contact
    publish_res = sns_client.publish(
        PhoneNumber=phone_num,
        Message="Your friend has arrived.",
    )
    return

def lambda_handler(event, context):
    # TODO implement
    email = email_from_token(event)
    # email = 'yl4735@columbia.edu'
    contact = get_contact(email)
    print(contact)
    send_SMS(contact)
    return {
        'headers': {'Access-Control-Allow-Origin': "*"},
        'statusCode': 200,
        'body': json.dumps('Message Sent!')
    }

