import json
import boto3
import ast

def get_Info(event):
    # get user's profile info from response
    # reuturn a dict
    print("!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!")
    body = event['body']
    print(type(body))
    body = ast.literal_eval(body)
    print(body)
    res = {
        'name': body['name'],
        'gender': body['gender'],
        'cellphone': body['cellphone'],
        'emergency_contact': body['emergency_contact'],
        'emergency_email': body['emergency_email']
    }
    return res
    
    
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
    
    
def update_DB(email, info):
    client = boto3.client('dynamodb')
    # delete the entity first, deleting non-exist entity will not cause error
    response = client.delete_item(
        TableName='user_profile',
        Key={
            'email': {
                'S': email
            }
        }
    )
    print("delete")
    print()
    # put entity into profile DB
    response = client.put_item(
        TableName='user_profile',
        Item={
            'email': {'S': email},
            'name': {'S': info['name']},
            'gender': {'S': info['gender']},
            'cellphone': {'N': info['cellphone']},
            'emergency_contact': {'N': info['emergency_contact']},
            'emergency_email': {'S': info['emergency_email']}
        }
    )
    print(response)
    return response

def check_if_new(email):
    client = boto3.client('dynamodb')
    response = client.get_item(
            TableName='user_profile',
            Key={
                'email': {
                    'S': email
                }
            }
        )
    print(response)
    if 'Item' in response.keys():
        return False
    return True
    
def lambda_handler(event, context):
    # TODO implement
    
    print(">>>")
    print(event)
    print("<<<")

    # event = {'resource': '/profile', 'path': '/profile', 'httpMethod': 'GET', 'headers': {'accept': '*/*', 'accept-encoding': 'gzip, deflate, br', 'accept-language': 'zh-CN,zh-Hans;q=0.9', 'content-type': 'application/json', 'Host': 'k9wj046mrd.execute-api.us-east-1.amazonaws.com', 'origin': 'https://6998frontendtest.s3.amazonaws.com', 'referer': 'https://6998frontendtest.s3.amazonaws.com/', 'token': 'eyJraWQiOiJ4Zk9sZTU2ZG5kTmNNUXY5eVMyeTAxeFFLM251TXFtakJZQlhmbkJVUFFrPSIsImFsZyI6IlJTMjU2In0.eyJhdF9oYXNoIjoicDJTNlEyR2FhR2JYcTgwUkQ5OFdTQSIsInN1YiI6IjNlMzEzYWVjLWNkNDUtNDUzOC05YjI4LTUyYWNiYjBhODc0MyIsImNvZ25pdG86Z3JvdXBzIjpbInVzLWVhc3QtMV8wck51b051YzRfR29vZ2xlIl0sImVtYWlsX3ZlcmlmaWVkIjp0cnVlLCJpc3MiOiJodHRwczpcL1wvY29nbml0by1pZHAudXMtZWFzdC0xLmFtYXpvbmF3cy5jb21cL3VzLWVhc3QtMV8wck51b051YzQiLCJjb2duaXRvOnVzZXJuYW1lIjoiZ29vZ2xlXzExMjQ1NjEzMzU4MDU5MjY3MjM4NCIsIm5vbmNlIjoidkNQOEVmZ25mVV9yXzk0aUN3eUdFVjBGN0hxeU5hZktwUUJOd3dXbENVQ2o5M296RjBaNE1Db0YwWThZV1EzVGJneUNGOGlicGoxa0NudkVWUzNFb2RiMVJaUGxVNTA2OFdwMTJ0V3V5dFdUbkhZS01sVE5XN1BWWGVCQ2gzdnctdXpLSDI0V2NsSWQ2blhXOThCZ21Lbk1wVy1uTzliN0cyXzY2aGFJd28wIiwiYXVkIjoidXVkb3A1amk0YTkzMGhkMmxkOGdpbzRxbiIsImlkZW50aXRpZXMiOlt7InVzZXJJZCI6IjExMjQ1NjEzMzU4MDU5MjY3MjM4NCIsInByb3ZpZGVyTmFtZSI6Ikdvb2dsZSIsInByb3ZpZGVyVHlwZSI6Ikdvb2dsZSIsImlzc3VlciI6bnVsbCwicHJpbWFyeSI6InRydWUiLCJkYXRlQ3JlYXRlZCI6IjE2Mzg1MDk1NjYzOTgifV0sInRva2VuX3VzZSI6ImlkIiwiYXV0aF90aW1lIjoxNjM4NjY0OTI2LCJuYW1lIjoiWWFuaGFvIExpIiwiZXhwIjoxNjM4NjY4NTI2LCJpYXQiOjE2Mzg2NjQ5MjYsImp0aSI6ImZkZmMzZWIxLTVhZjItNGY0MS1hZDc0LTdmMmRkOWI0NmI0NSIsImVtYWlsIjoieWw0NzM1QGNvbHVtYmlhLmVkdSJ9.i9RWq4C2J5sFIZGGkTkU-zXtEoZYE2FJ6s6GpFeNeJGJhBpCv3vp5zy_ijJycAo2kQBIoX39faGvREO9u1TH45EXOr4BLkfWpuiDtAlJsd9Fxxs3nbwmXMT002GC7S3mcxgeI_ZNtD7d-25x-6F9Rofyar_OZ78y8bXKfg9NUS5Oj5fr7rzW_QPPkL9zN5_4OgDEiv64GnW2ZMoqb-8GIe8uESPe5zuvK9ijEo6atmUB3Ejc3nZOKs49BzXN-_F_dxJqLAvXcNCoWkVGmGuB0OxsLqI8rG25MKTN4WRugJW8gnQVjwC4BHQE_YdJGfRTK04bMJus5HPMXekYW9kbXA', 'User-Agent': 'Mozilla/5.0 (iPhone; CPU iPhone OS 15_1 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) CriOS/96.0.4664.53 Mobile/15E148 Safari/604.1', 'X-Amzn-Trace-Id': 'Root=1-61ac0ae0-5d49b98736c98d382970d535', 'X-Forwarded-For': '107.127.42.128', 'X-Forwarded-Port': '443', 'X-Forwarded-Proto': 'https'}, 'multiValueHeaders': {'accept': ['*/*'], 'accept-encoding': ['gzip, deflate, br'], 'accept-language': ['zh-CN,zh-Hans;q=0.9'], 'content-type': ['application/json'], 'Host': ['k9wj046mrd.execute-api.us-east-1.amazonaws.com'], 'origin': ['https://6998frontendtest.s3.amazonaws.com'], 'referer': ['https://6998frontendtest.s3.amazonaws.com/'], 'token': ['eyJraWQiOiJ4Zk9sZTU2ZG5kTmNNUXY5eVMyeTAxeFFLM251TXFtakJZQlhmbkJVUFFrPSIsImFsZyI6IlJTMjU2In0.eyJhdF9oYXNoIjoicDJTNlEyR2FhR2JYcTgwUkQ5OFdTQSIsInN1YiI6IjNlMzEzYWVjLWNkNDUtNDUzOC05YjI4LTUyYWNiYjBhODc0MyIsImNvZ25pdG86Z3JvdXBzIjpbInVzLWVhc3QtMV8wck51b051YzRfR29vZ2xlIl0sImVtYWlsX3ZlcmlmaWVkIjp0cnVlLCJpc3MiOiJodHRwczpcL1wvY29nbml0by1pZHAudXMtZWFzdC0xLmFtYXpvbmF3cy5jb21cL3VzLWVhc3QtMV8wck51b051YzQiLCJjb2duaXRvOnVzZXJuYW1lIjoiZ29vZ2xlXzExMjQ1NjEzMzU4MDU5MjY3MjM4NCIsIm5vbmNlIjoidkNQOEVmZ25mVV9yXzk0aUN3eUdFVjBGN0hxeU5hZktwUUJOd3dXbENVQ2o5M296RjBaNE1Db0YwWThZV1EzVGJneUNGOGlicGoxa0NudkVWUzNFb2RiMVJaUGxVNTA2OFdwMTJ0V3V5dFdUbkhZS01sVE5XN1BWWGVCQ2gzdnctdXpLSDI0V2NsSWQ2blhXOThCZ21Lbk1wVy1uTzliN0cyXzY2aGFJd28wIiwiYXVkIjoidXVkb3A1amk0YTkzMGhkMmxkOGdpbzRxbiIsImlkZW50aXRpZXMiOlt7InVzZXJJZCI6IjExMjQ1NjEzMzU4MDU5MjY3MjM4NCIsInByb3ZpZGVyTmFtZSI6Ikdvb2dsZSIsInByb3ZpZGVyVHlwZSI6Ikdvb2dsZSIsImlzc3VlciI6bnVsbCwicHJpbWFyeSI6InRydWUiLCJkYXRlQ3JlYXRlZCI6IjE2Mzg1MDk1NjYzOTgifV0sInRva2VuX3VzZSI6ImlkIiwiYXV0aF90aW1lIjoxNjM4NjY0OTI2LCJuYW1lIjoiWWFuaGFvIExpIiwiZXhwIjoxNjM4NjY4NTI2LCJpYXQiOjE2Mzg2NjQ5MjYsImp0aSI6ImZkZmMzZWIxLTVhZjItNGY0MS1hZDc0LTdmMmRkOWI0NmI0NSIsImVtYWlsIjoieWw0NzM1QGNvbHVtYmlhLmVkdSJ9.i9RWq4C2J5sFIZGGkTkU-zXtEoZYE2FJ6s6GpFeNeJGJhBpCv3vp5zy_ijJycAo2kQBIoX39faGvREO9u1TH45EXOr4BLkfWpuiDtAlJsd9Fxxs3nbwmXMT002GC7S3mcxgeI_ZNtD7d-25x-6F9Rofyar_OZ78y8bXKfg9NUS5Oj5fr7rzW_QPPkL9zN5_4OgDEiv64GnW2ZMoqb-8GIe8uESPe5zuvK9ijEo6atmUB3Ejc3nZOKs49BzXN-_F_dxJqLAvXcNCoWkVGmGuB0OxsLqI8rG25MKTN4WRugJW8gnQVjwC4BHQE_YdJGfRTK04bMJus5HPMXekYW9kbXA'], 'User-Agent': ['Mozilla/5.0 (iPhone; CPU iPhone OS 15_1 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) CriOS/96.0.4664.53 Mobile/15E148 Safari/604.1'], 'X-Amzn-Trace-Id': ['Root=1-61ac0ae0-5d49b98736c98d382970d535'], 'X-Forwarded-For': ['107.127.42.128'], 'X-Forwarded-Port': ['443'], 'X-Forwarded-Proto': ['https']}, 'queryStringParameters': {'_': '1638664928377', 'accessToken': 'eyJraWQiOiI4UkY1TDZtdEhGQlBFRkNaSFFPeGxFY2p6azVIVGNaQWZ6a1lLUG9LS3VzPSIsImFsZyI6IlJTMjU2In0.eyJzdWIiOiIzZTMxM2FlYy1jZDQ1LTQ1MzgtOWIyOC01MmFjYmIwYTg3NDMiLCJjb2duaXRvOmdyb3VwcyI6WyJ1cy1lYXN0LTFfMHJOdW9OdWM0X0dvb2dsZSJdLCJ0b2tlbl91c2UiOiJhY2Nlc3MiLCJzY29wZSI6ImF3cy5jb2duaXRvLnNpZ25pbi51c2VyLmFkbWluIHBob25lIG9wZW5pZCBwcm9maWxlIGVtYWlsIiwiYXV0aF90aW1lIjoxNjM4NjY0OTI2LCJpc3MiOiJodHRwczpcL1wvY29nbml0by1pZHAudXMtZWFzdC0xLmFtYXpvbmF3cy5jb21cL3VzLWVhc3QtMV8wck51b051YzQiLCJleHAiOjE2Mzg2Njg1MjYsImlhdCI6MTYzODY2NDkyNiwidmVyc2lvbiI6MiwianRpIjoiMTU3OGZmNzItYWQ4Ny00OTlmLWE1MzQtNTRkNjRlYTFmZjJhIiwiY2xpZW50X2lkIjoidXVkb3A1amk0YTkzMGhkMmxkOGdpbzRxbiIsInVzZXJuYW1lIjoiZ29vZ2xlXzExMjQ1NjEzMzU4MDU5MjY3MjM4NCJ9.c0v6U8iljd4ayBwc27-rV3nU5sjxIkkjd_g6BbmgN87EyjiVs_0Ql0Q-LZs2TbpH4aKBSp_Tnk8c7bSRglzgRD_-vKiRARGCVnTMmP5Sm_TwWLhbftzvtXVgcEEOcXESVE0R37ZM17PGUtrbwvIkA6l0B0BLVbesiY4SUfGTLwnOqexYCNH-3JPBtK91jIhg_oOItUtWLIGCYF_XDalo7bptyB7Z1peuNSaS1ttpHPZwvbTs3g-ElpK2fCy7RWOJlbjSfqJ5-wwaVSURQcKOGP_Gl7dQieei6vZGSKMWlhlQb8rnoVMZ38I-KLoJC7aVkelx73f6hYIwgkShaStrzg'}, 'multiValueQueryStringParameters': {'_': ['1638664928377'], 'accessToken': ['eyJraWQiOiI4UkY1TDZtdEhGQlBFRkNaSFFPeGxFY2p6azVIVGNaQWZ6a1lLUG9LS3VzPSIsImFsZyI6IlJTMjU2In0.eyJzdWIiOiIzZTMxM2FlYy1jZDQ1LTQ1MzgtOWIyOC01MmFjYmIwYTg3NDMiLCJjb2duaXRvOmdyb3VwcyI6WyJ1cy1lYXN0LTFfMHJOdW9OdWM0X0dvb2dsZSJdLCJ0b2tlbl91c2UiOiJhY2Nlc3MiLCJzY29wZSI6ImF3cy5jb2duaXRvLnNpZ25pbi51c2VyLmFkbWluIHBob25lIG9wZW5pZCBwcm9maWxlIGVtYWlsIiwiYXV0aF90aW1lIjoxNjM4NjY0OTI2LCJpc3MiOiJodHRwczpcL1wvY29nbml0by1pZHAudXMtZWFzdC0xLmFtYXpvbmF3cy5jb21cL3VzLWVhc3QtMV8wck51b051YzQiLCJleHAiOjE2Mzg2Njg1MjYsImlhdCI6MTYzODY2NDkyNiwidmVyc2lvbiI6MiwianRpIjoiMTU3OGZmNzItYWQ4Ny00OTlmLWE1MzQtNTRkNjRlYTFmZjJhIiwiY2xpZW50X2lkIjoidXVkb3A1amk0YTkzMGhkMmxkOGdpbzRxbiIsInVzZXJuYW1lIjoiZ29vZ2xlXzExMjQ1NjEzMzU4MDU5MjY3MjM4NCJ9.c0v6U8iljd4ayBwc27-rV3nU5sjxIkkjd_g6BbmgN87EyjiVs_0Ql0Q-LZs2TbpH4aKBSp_Tnk8c7bSRglzgRD_-vKiRARGCVnTMmP5Sm_TwWLhbftzvtXVgcEEOcXESVE0R37ZM17PGUtrbwvIkA6l0B0BLVbesiY4SUfGTLwnOqexYCNH-3JPBtK91jIhg_oOItUtWLIGCYF_XDalo7bptyB7Z1peuNSaS1ttpHPZwvbTs3g-ElpK2fCy7RWOJlbjSfqJ5-wwaVSURQcKOGP_Gl7dQieei6vZGSKMWlhlQb8rnoVMZ38I-KLoJC7aVkelx73f6hYIwgkShaStrzg']}, 'pathParameters': None, 'stageVariables': None, 'requestContext': {'resourceId': 'zgempl', 'resourcePath': '/profile', 'httpMethod': 'GET', 'extendedRequestId': 'J2ajKHJRoAMF64Q=', 'requestTime': '05/Dec/2021:00:42:08 +0000', 'path': '/6998FirstTry/profile', 'accountId': '680019774401', 'protocol': 'HTTP/1.1', 'stage': '6998FirstTry', 'domainPrefix': 'k9wj046mrd', 'requestTimeEpoch': 1638664928866, 'requestId': '3e99fcd3-e3b3-4bc6-9d81-c043868c3d0f', 'identity': {'cognitoIdentityPoolId': None, 'accountId': None, 'cognitoIdentityId': None, 'caller': None, 'sourceIp': '107.127.42.128', 'principalOrgId': None, 'accessKey': None, 'cognitoAuthenticationType': None, 'cognitoAuthenticationProvider': None, 'userArn': None, 'userAgent': 'Mozilla/5.0 (iPhone; CPU iPhone OS 15_1 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) CriOS/96.0.4664.53 Mobile/15E148 Safari/604.1', 'user': None}, 'domainName': 'k9wj046mrd.execute-api.us-east-1.amazonaws.com', 'apiId': 'k9wj046mrd'}, 'body': None, 'isBase64Encoded': False}
    
    method = event['httpMethod']
    
    if method == 'POST':
        info = get_Info(event)
        email = email_from_token(event)    
        print('info')
        print(info)
        print('email')
        print(email)
        update_DB(email, info)
        return {
            'headers': {'Access-Control-Allow-Origin': "*"},
            'statusCode': 200,
            'body': json.dumps('post success')
        }
    if method == 'GET':
        # first check if old user, if not create a profile only with email
        email = email_from_token(event)
        new_user = check_if_new(email)
        if new_user:
            # create profile only with email, empty info
            empty = {
                        'name': '',
                        'gender': '',
                        'cellphone': '',
                        'emergency_contact': '',
                        'emergency_email': ''
                    }
            update_DB(email, empty)
        # get user profile from DB
        client = boto3.client('dynamodb')
        response = client.get_item(
        TableName='user_profile',
        Key={
            'email': {
                'S': email
                }
        })
        
        print(response)
        res = response['Item']
        return {
            'headers': {'Access-Control-Allow-Origin': "*"},
            'statusCode': 200,
            'body': json.dumps(res)
        }
    return {
            'headers': {'Access-Control-Allow-Origin': "*"},
            'statusCode': 200,
            'body': json.dumps('not valid method')
        }
            
        
def test():
    res = check_if_new('abc')
    print(res)