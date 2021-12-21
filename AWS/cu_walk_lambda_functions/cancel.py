import json
import boto3


def email_from_token(event):
    # get user email from token, email is primary key in DB
    access_token = event['queryStringParameters']['accessToken']
    client = boto3.client('cognito-idp')
    response = client.get_user(
        AccessToken=access_token
    )
    for d in response['UserAttributes']:
        if d['Name'] == 'email':
            email = d['Value']
    user_info = {
        'Username': response['Username'],
        'Email': email
    }
    print(user_info)
    return user_info['Email']
    
def delete_trip(email):
    client = boto3.client('dynamodb')
    response = client.delete_item(
        TableName='individual_trip',
        Key={
            'email': {
                'S': email
            }
        }
    )
    print("deleted trip ")
    return response

def delete_from_group(email):
    TABLE_NAME = "groups"
    client = boto3.resource('dynamodb')
    table = client.Table(TABLE_NAME)
    response = table.scan()
    groups = response['Items']
    for g in groups:
        teamates = json.loads(g['teamates'])['value']
        if email in teamates:
            if len(teamates)>1:
                teamates.remove(email)
                g['teamates'] = json.dumps({'value': teamates})
                response = table.update_item(
                    Key={
                        'first_user_coordinate': g['first_user_coordinate'],
                        'time': g['time']
                    },
                    UpdateExpression='SET teamates = :val1',
                    ExpressionAttributeValues={
                        ':val1': g['teamates']
                    }
                )
                
                # response = client.put_item(
                #     TableName='groups',
                #     Item=g
                # )
                print("remove user from group")
                return g
            else:
                # delete the group if user is the only one in the group
                print(g)
                response = table.delete_item(
                    TableName='groups',
                    Key={
                        'first_user_coordinate': g['first_user_coordinate'],
                        'time': g['time']
                    }
                )
                print("delete group")
                print(response)
                return response
    print("no group find")
    return False
    
def monitor_status_off(email):
    TABLE_NAME = "monitor"
    client = boto3.resource('dynamodb')
    table = client.Table(TABLE_NAME)
    response = table.update_item(
                    Key={
                        "user_email": email
                    },
                    UpdateExpression='SET monitor_status = :val1',
                    ExpressionAttributeValues={
                        ':val1': "off"
                    }
                )
    return response
    
def lambda_handler(event, context):
    # TODO implement
    print(">>>")
    print(event)
    print("<<<")
    email = email_from_token(event)
    # email = "cs4091@columbia.edu"
    delete_trip(email)
    delete_from_group(email)
    monitor_status_off(email)
    monitor_status_off(email)
    return {
        'headers': {'Access-Control-Allow-Origin': "*"},
        'statusCode': 200,
        'body': json.dumps('cancel sucess')
    }
