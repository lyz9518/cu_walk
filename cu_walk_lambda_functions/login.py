import json
import boto3


# db doc: https://boto3.amazonaws.com/v1/documentation/api/latest/guide/dynamodb.html

# def isRegistered(user_id):
#     client = boto3.client('dynamodb')
#     response = client.get_item(
#         Key={
#             'user_id': user_id,
#             'last_name': 'Doe'
#         }
#     )
#     # TODO: check the format of response
#     print(response)
#     return False
#
#
# def lambda_handler(event, context):
#     client = boto3.client('dynamodb')
#     token = event['token']
#     CLIENT_ID = '726424026813-dnp9hgvuu9useqedh0kk33v32agnkbrq'
#     try:
#         # Specify the CLIENT_ID of the app that accesses the backend:
#         idinfo = id_token.verify_oauth2_token(token, requests.Request(), CLIENT_ID)
#
#         # Or, if multiple clients access the backend server:
#         # idinfo = id_token.verify_oauth2_token(token, requests.Request())
#         # if idinfo['aud'] not in [CLIENT_ID_1, CLIENT_ID_2, CLIENT_ID_3]:
#         #     raise ValueError('Could not verify audience.')
#
#         # If auth request is from a G Suite domain:
#         # if idinfo['hd'] != GSUITE_DOMAIN_NAME:
#         #     raise ValueError('Wrong hosted domain.')
#
#         # ID token is valid. Get the user's Google Account ID from the decoded token.
#         user_id = idinfo['sub']
#     except ValueError:
#         # Invalid token
#         print("invalid token!!!!!!")
#         return json.dumps({
#             'statusCode': 403,
#             'body': json.dumps('Invalid token')
#         })
#     if isRegistered(user_id):
#         return json.dumps({
#             'statusCode': 200,
#             'body': json.dumps('User log in successfully')
#         })
#     else:
#         return json.dumps({
#             'statusCode': 200,
#             'body': json.dumps('User is not created, automatically creating one and then log in....')
#         })

# get querystring from url
# https://stackoverflow.com/questions/31329958/how-to-pass-a-querystring-or-route-parameter-to-aws-lambda-from-amazon-api-gatew
def lambda_handler(event, context):
    access_token = event['queryStringParameters']['accessToken']
    client = boto3.client('cognito-idp')
    response = client.get_user(
        AccessToken=access_token
    )
    email = ""
    for d in response['UserAttributes']:
        if d['Name'] == 'email':
            email = d['Value']
    print(response)
    result_dict = {
        'Username': response['Username'],
        'Email': email
    }
    print(event)
    return {
        'headers': {'Access-Control-Allow-Origin': "*"},
        'statusCode': 200,
        'body': json.dumps(result_dict)
    }
