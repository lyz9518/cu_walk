import json
import boto3
import googlemaps
from boto3.dynamodb.conditions import Attr
import ast
import random
import time
# This lambda recieves access token, trip information
# It put individial trip information into DB individual_trip.
# It create a new empty group for the user

def email_from_token(token):
    # get user email from token, email is primary key in DB
    client = boto3.client('cognito-idp')
    response = client.get_user(
    AccessToken=token
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

    
def get_trip_info(event):
    body = event['body']
    body = ast.literal_eval(body)
    # print(body)
    res = {
        "time": body['time'],
        "departure": body['departure'],
        "destination": body['destination']
    }
    return res
        
def put_trip(email, info):
    # put the trip into individual_trip DB with email as partition key
    client = boto3.client('dynamodb')
    # deletes the entity first, makes sure every user can only have one trip, deleting non-exist entity will not cause error
    response = client.delete_item(
        TableName='individual_trip',
        Key={
            'email': {
                'S': email
            }
        }
    )
    
    response = client.put_item(
            TableName='individual_trip',
            Item={
                'email': {'S': email},
                'time': {'S': info['time']},
                'departure': {'S': info['departure']},
                'destination': {'S': json.dumps(info['destination'])}
            }
        )
    print(response)
    return response

def find_satisfied_groups(email, info):
    # group DB attributes: time, departure, teamates, first_user_coordinate
    # the function will find a group first based on time  then makes sure the existing group destination is within 500m
    # if no satisfied group exists, create a new one with size 0
    
    # get the list of groups with same time and departure
    TABLE_NAME = "groups"
    time = info['time']
    departure = info['departure']
    
    client = boto3.resource('dynamodb')
    table = client.Table(TABLE_NAME)
    response = table.scan(
        FilterExpression=Attr('time').eq(time)
        )
        
    groups = response['Items'] # groups with same departure time
    print(response['Items'])
    satisfied_groups = []
    for group in groups:
        distance = calculate_distance(group["first_user_coordinate"], info["destination"])
        if distance < 800:
            satisfied_groups.append(group)
    return satisfied_groups

def calculate_distance(origin, destination):
    API_key = "AIzaSyDrVTUpcyFC5ZdYLszLJNe4wB17g_dAc4A"
    gmaps = googlemaps.Client(key=API_key)
    ori = json.loads(origin)
    ori_coord = (ori['latitude'], ori['longitude'])
    desti = destination
    print("!!!!!!!!!desti")
    print(desti)
    print("!!!!!!!!!desti")
    desti = (desti['latitude'], desti['longitude'])
    result = gmaps.distance_matrix(ori, desti, mode='walking')
    d = result["rows"][0]["elements"][0]
    if 'status' in d.keys() and d['status'] == 'ZERO_RESULTS':
        print('invalid address')
        return 600
    # print(result["rows"][0]["elements"])
    print("!!!!!!!!!!!!!!")
    print(result["rows"][0]["elements"][0]["distance"]["value"])
    return result["rows"][0]["elements"][0]["distance"]["value"]
    

def create_group(email, info):
    # create an empty group with user info
    code = random.randint(1000,9999)
    client = boto3.client('dynamodb')
    teamates = json.dumps({'value': []})
    response = client.put_item(
            TableName='groups',
            Item={
                'time': {'S': info['time']},
                'departure': {'S': info['departure']},
                'first_user_coordinate': {'S': json.dumps(info['destination'])},
                'teamates': {'S': teamates},
                'code': {'S': str(code)}
            }
        )
    print(response)
    print(code)
    return response
    
# def insert_to_groups(email, groups):
#     group_partition_keys = [g['first_user_coordinate'] for g in groups]
#     # print(group_partition_keys)
#     tp_groups = pop_by_keys(group_partition_keys)
#     print(tp_groups)
#     tp_groups = [{'teamates': {'S': '{"value": ["abc"]}'}, 'time': {'S': '800'}, 'departure': {'S': 'dep'}, 'team_size': {'N': '1'}, 'first_user_coordinate': {'S': '{"latitude": -10.9393, "longitude": -37.0627}'}}, {'teamates': {'S': '{"value": ["abc"]}'}, 'time': {'S': '800'}, 'departure': {'S': 'app'}, 'team_size': {'N': '1'}, 'first_user_coordinate': {'S': '{"latitude": -10.9393, "longitude": -37.0629}'}}]
#     for g in tp_groups:
#         value_dict = json.loads(g["teamates"]["S"])
#         value_dict['value'].append(email)
#         g["teamates"]["S"] = json.dumps(value_dict)
#         g["team_size"]["N"] = str(int(g["team_size"]["N"])+1)
#         print(g)
#         client = boto3.client('dynamodb')
#         response = client.put_item(
#             TableName='group',
#             Item=g
#         )
#     return
# def pop_by_keys(keys):
#     client = boto3.client('dynamodb')
#     # delete the entity first, deleting non-exist entity will not cause error
#     res = []
#     for k in keys:
#         r1 = client.get_item(
#             TableName='group',
#             Key={
#                 'first_user_coordinate': {
#                     'S': k
#                 }
#             }
#         )
#         res.append(r1['Item'])
#         response = client.delete_item(
#             TableName='group',
#             Key={
#                 'first_user_coordinate': {
#                     'S': k
#                 }
#             }
#         )
#     return res
    
def lambda_handler(event, context):
    print(">>>")
    print(event)
    print("<<<")
    # event = {'resource': '/trip', 'path': '/trip', 'httpMethod': 'POST', 'headers': {'accept': '*/*', 'accept-encoding': 'gzip, deflate, br', 'accept-language': 'zh-CN,zh-Hans;q=0.9', 'content-type': 'application/json', 'Host': 'k9wj046mrd.execute-api.us-east-1.amazonaws.com', 'origin': 'https://6998frontendtest.s3.amazonaws.com', 'referer': 'https://6998frontendtest.s3.amazonaws.com/', 'token': 'eyJraWQiOiJ4Zk9sZTU2ZG5kTmNNUXY5eVMyeTAxeFFLM251TXFtakJZQlhmbkJVUFFrPSIsImFsZyI6IlJTMjU2In0.eyJhdF9oYXNoIjoid1hDR2FILUxQZlNtdTVXTFJMVk5zdyIsInN1YiI6IjNlMzEzYWVjLWNkNDUtNDUzOC05YjI4LTUyYWNiYjBhODc0MyIsImNvZ25pdG86Z3JvdXBzIjpbInVzLWVhc3QtMV8wck51b051YzRfR29vZ2xlIl0sImVtYWlsX3ZlcmlmaWVkIjp0cnVlLCJpc3MiOiJodHRwczpcL1wvY29nbml0by1pZHAudXMtZWFzdC0xLmFtYXpvbmF3cy5jb21cL3VzLWVhc3QtMV8wck51b051YzQiLCJjb2duaXRvOnVzZXJuYW1lIjoiZ29vZ2xlXzExMjQ1NjEzMzU4MDU5MjY3MjM4NCIsIm5vbmNlIjoiX01KOEtlUWEzSmN6VXdCYWJQZlZUb1hHcWd3RFBxam9GVHowOUZ4aTFqbDhjWDFBWU13enlDOXdZM3pDLXcycXljcXU2eW1sWHpTUnZ0QjRPc2VyUExWa0xJczZSUmRseWxiRGxWUXBsNjNKUG93ZGVKejJpYkRDVEVFOVY4ZGhqQUdOMkVET1duSTgxLUptZHRlSDVSdzlLcTFqZTlFVzJZNkxrTWpZeG93IiwiYXVkIjoidXVkb3A1amk0YTkzMGhkMmxkOGdpbzRxbiIsImlkZW50aXRpZXMiOlt7InVzZXJJZCI6IjExMjQ1NjEzMzU4MDU5MjY3MjM4NCIsInByb3ZpZGVyTmFtZSI6Ikdvb2dsZSIsInByb3ZpZGVyVHlwZSI6Ikdvb2dsZSIsImlzc3VlciI6bnVsbCwicHJpbWFyeSI6InRydWUiLCJkYXRlQ3JlYXRlZCI6IjE2Mzg1MDk1NjYzOTgifV0sInRva2VuX3VzZSI6ImlkIiwiYXV0aF90aW1lIjoxNjM4NzAwMzEzLCJuYW1lIjoiWWFuaGFvIExpIiwiZXhwIjoxNjM4NzAzOTEzLCJpYXQiOjE2Mzg3MDAzMTMsImp0aSI6IjRlOGE5MmJmLWYxOTQtNDg3My1iYzU0LWQ2ZDIwZDI2MDA2YyIsImVtYWlsIjoieWw0NzM1QGNvbHVtYmlhLmVkdSJ9.jb8ViYQeqGvKv7_UBQMO7Pqcl_kVRU_hlHEw_CmIwKuyCqGfE9yQHGP5DYWZlk3N2E9PEsaQ94dzZ9rgUC8AAAz7v2tlocHybtuS_jEhrQZPnyKtFL_h8CQygTufW3xgV5bx2IdLTQYt8nedu0yJ239ut3xrSK9aqc-Yax97D6P7uZJgvcu2p85bq3KmYugy0xBPR7FccArlfQkx3-GTSEx0FWE9rVbprC8NdstApWGWFAgyk_iX1YlnHZzopV3C3eVWmhSm5tISATbzzeKw0IUhmiDinoCYa7ZgIreCRahmNOquSdcfHSUzKcXG6oazT3zZl8x4-nGjG_tjpggtJA', 'User-Agent': 'Mozilla/5.0 (iPhone; CPU iPhone OS 15_1_1 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/15.1 Mobile/15E148 Safari/604.1', 'X-Amzn-Trace-Id': 'Root=1-61ac9538-32135bc1527bcec3735de93e', 'X-Forwarded-For': '98.15.66.96', 'X-Forwarded-Port': '443', 'X-Forwarded-Proto': 'https'}, 'multiValueHeaders': {'accept': ['*/*'], 'accept-encoding': ['gzip, deflate, br'], 'accept-language': ['zh-CN,zh-Hans;q=0.9'], 'content-type': ['application/json'], 'Host': ['k9wj046mrd.execute-api.us-east-1.amazonaws.com'], 'origin': ['https://6998frontendtest.s3.amazonaws.com'], 'referer': ['https://6998frontendtest.s3.amazonaws.com/'], 'token': ['eyJraWQiOiJ4Zk9sZTU2ZG5kTmNNUXY5eVMyeTAxeFFLM251TXFtakJZQlhmbkJVUFFrPSIsImFsZyI6IlJTMjU2In0.eyJhdF9oYXNoIjoid1hDR2FILUxQZlNtdTVXTFJMVk5zdyIsInN1YiI6IjNlMzEzYWVjLWNkNDUtNDUzOC05YjI4LTUyYWNiYjBhODc0MyIsImNvZ25pdG86Z3JvdXBzIjpbInVzLWVhc3QtMV8wck51b051YzRfR29vZ2xlIl0sImVtYWlsX3ZlcmlmaWVkIjp0cnVlLCJpc3MiOiJodHRwczpcL1wvY29nbml0by1pZHAudXMtZWFzdC0xLmFtYXpvbmF3cy5jb21cL3VzLWVhc3QtMV8wck51b051YzQiLCJjb2duaXRvOnVzZXJuYW1lIjoiZ29vZ2xlXzExMjQ1NjEzMzU4MDU5MjY3MjM4NCIsIm5vbmNlIjoiX01KOEtlUWEzSmN6VXdCYWJQZlZUb1hHcWd3RFBxam9GVHowOUZ4aTFqbDhjWDFBWU13enlDOXdZM3pDLXcycXljcXU2eW1sWHpTUnZ0QjRPc2VyUExWa0xJczZSUmRseWxiRGxWUXBsNjNKUG93ZGVKejJpYkRDVEVFOVY4ZGhqQUdOMkVET1duSTgxLUptZHRlSDVSdzlLcTFqZTlFVzJZNkxrTWpZeG93IiwiYXVkIjoidXVkb3A1amk0YTkzMGhkMmxkOGdpbzRxbiIsImlkZW50aXRpZXMiOlt7InVzZXJJZCI6IjExMjQ1NjEzMzU4MDU5MjY3MjM4NCIsInByb3ZpZGVyTmFtZSI6Ikdvb2dsZSIsInByb3ZpZGVyVHlwZSI6Ikdvb2dsZSIsImlzc3VlciI6bnVsbCwicHJpbWFyeSI6InRydWUiLCJkYXRlQ3JlYXRlZCI6IjE2Mzg1MDk1NjYzOTgifV0sInRva2VuX3VzZSI6ImlkIiwiYXV0aF90aW1lIjoxNjM4NzAwMzEzLCJuYW1lIjoiWWFuaGFvIExpIiwiZXhwIjoxNjM4NzAzOTEzLCJpYXQiOjE2Mzg3MDAzMTMsImp0aSI6IjRlOGE5MmJmLWYxOTQtNDg3My1iYzU0LWQ2ZDIwZDI2MDA2YyIsImVtYWlsIjoieWw0NzM1QGNvbHVtYmlhLmVkdSJ9.jb8ViYQeqGvKv7_UBQMO7Pqcl_kVRU_hlHEw_CmIwKuyCqGfE9yQHGP5DYWZlk3N2E9PEsaQ94dzZ9rgUC8AAAz7v2tlocHybtuS_jEhrQZPnyKtFL_h8CQygTufW3xgV5bx2IdLTQYt8nedu0yJ239ut3xrSK9aqc-Yax97D6P7uZJgvcu2p85bq3KmYugy0xBPR7FccArlfQkx3-GTSEx0FWE9rVbprC8NdstApWGWFAgyk_iX1YlnHZzopV3C3eVWmhSm5tISATbzzeKw0IUhmiDinoCYa7ZgIreCRahmNOquSdcfHSUzKcXG6oazT3zZl8x4-nGjG_tjpggtJA'], 'User-Agent': ['Mozilla/5.0 (iPhone; CPU iPhone OS 15_1_1 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/15.1 Mobile/15E148 Safari/604.1'], 'X-Amzn-Trace-Id': ['Root=1-61ac9538-32135bc1527bcec3735de93e'], 'X-Forwarded-For': ['98.15.66.96'], 'X-Forwarded-Port': ['443'], 'X-Forwarded-Proto': ['https']}, 'queryStringParameters': {'accessToken': 'eyJraWQiOiI4UkY1TDZtdEhGQlBFRkNaSFFPeGxFY2p6azVIVGNaQWZ6a1lLUG9LS3VzPSIsImFsZyI6IlJTMjU2In0.eyJzdWIiOiIzZTMxM2FlYy1jZDQ1LTQ1MzgtOWIyOC01MmFjYmIwYTg3NDMiLCJjb2duaXRvOmdyb3VwcyI6WyJ1cy1lYXN0LTFfMHJOdW9OdWM0X0dvb2dsZSJdLCJ0b2tlbl91c2UiOiJhY2Nlc3MiLCJzY29wZSI6ImF3cy5jb2duaXRvLnNpZ25pbi51c2VyLmFkbWluIHBob25lIG9wZW5pZCBwcm9maWxlIGVtYWlsIiwiYXV0aF90aW1lIjoxNjM4NzAwMzEzLCJpc3MiOiJodHRwczpcL1wvY29nbml0by1pZHAudXMtZWFzdC0xLmFtYXpvbmF3cy5jb21cL3VzLWVhc3QtMV8wck51b051YzQiLCJleHAiOjE2Mzg3MDM5MTMsImlhdCI6MTYzODcwMDMxMywidmVyc2lvbiI6MiwianRpIjoiNmMxMGM5NDYtMjcxZS00NDk4LWFiNTQtNDEyYjMwMzIzZTM5IiwiY2xpZW50X2lkIjoidXVkb3A1amk0YTkzMGhkMmxkOGdpbzRxbiIsInVzZXJuYW1lIjoiZ29vZ2xlXzExMjQ1NjEzMzU4MDU5MjY3MjM4NCJ9.stuOhaRK-_grybcGGoG9CkQo0EuDO4_rfGsPoW2Oor_FRvLj_2T52ufTQHUF_tRZch7LyBUpjqoxT-kZbV0SGRFVXdKiF6w8ROp1UfJ6xQ-HsCB2Q6wFPJ4sszlvd_0N3byZcs8oGfKh-kdORet2hP-JAs_rT0d-PNQHXfjQWYyjNb1SBiIwc5YJ7dldYp-EX-nFH9hStAxfEOc99vtqm2NtJmrLI06DEUzD2A3bTudlFVUHJb4fz657s8nTxN6aEJxHWbAjootnaFA89_swY_K0u99K3XXON9E55JmXCV5ZtI2Pit0OetC9A8lT88oXVafhFIqRH15z07KO2avVpg'}, 'multiValueQueryStringParameters': {'accessToken': ['eyJraWQiOiI4UkY1TDZtdEhGQlBFRkNaSFFPeGxFY2p6azVIVGNaQWZ6a1lLUG9LS3VzPSIsImFsZyI6IlJTMjU2In0.eyJzdWIiOiIzZTMxM2FlYy1jZDQ1LTQ1MzgtOWIyOC01MmFjYmIwYTg3NDMiLCJjb2duaXRvOmdyb3VwcyI6WyJ1cy1lYXN0LTFfMHJOdW9OdWM0X0dvb2dsZSJdLCJ0b2tlbl91c2UiOiJhY2Nlc3MiLCJzY29wZSI6ImF3cy5jb2duaXRvLnNpZ25pbi51c2VyLmFkbWluIHBob25lIG9wZW5pZCBwcm9maWxlIGVtYWlsIiwiYXV0aF90aW1lIjoxNjM4NzAwMzEzLCJpc3MiOiJodHRwczpcL1wvY29nbml0by1pZHAudXMtZWFzdC0xLmFtYXpvbmF3cy5jb21cL3VzLWVhc3QtMV8wck51b051YzQiLCJleHAiOjE2Mzg3MDM5MTMsImlhdCI6MTYzODcwMDMxMywidmVyc2lvbiI6MiwianRpIjoiNmMxMGM5NDYtMjcxZS00NDk4LWFiNTQtNDEyYjMwMzIzZTM5IiwiY2xpZW50X2lkIjoidXVkb3A1amk0YTkzMGhkMmxkOGdpbzRxbiIsInVzZXJuYW1lIjoiZ29vZ2xlXzExMjQ1NjEzMzU4MDU5MjY3MjM4NCJ9.stuOhaRK-_grybcGGoG9CkQo0EuDO4_rfGsPoW2Oor_FRvLj_2T52ufTQHUF_tRZch7LyBUpjqoxT-kZbV0SGRFVXdKiF6w8ROp1UfJ6xQ-HsCB2Q6wFPJ4sszlvd_0N3byZcs8oGfKh-kdORet2hP-JAs_rT0d-PNQHXfjQWYyjNb1SBiIwc5YJ7dldYp-EX-nFH9hStAxfEOc99vtqm2NtJmrLI06DEUzD2A3bTudlFVUHJb4fz657s8nTxN6aEJxHWbAjootnaFA89_swY_K0u99K3XXON9E55JmXCV5ZtI2Pit0OetC9A8lT88oXVafhFIqRH15z07KO2avVpg']}, 'pathParameters': None, 'stageVariables': None, 'requestContext': {'resourceId': 'te1ctj', 'resourcePath': '/trip', 'httpMethod': 'POST', 'extendedRequestId': 'J3xA5GGFoAMFuug=', 'requestTime': '05/Dec/2021:10:32:24 +0000', 'path': '/6998FirstTry/trip', 'accountId': '680019774401', 'protocol': 'HTTP/1.1', 'stage': '6998FirstTry', 'domainPrefix': 'k9wj046mrd', 'requestTimeEpoch': 1638700344758, 'requestId': '5fd7b09a-9309-44db-a958-1dba8f379b5b', 'identity': {'cognitoIdentityPoolId': None, 'accountId': None, 'cognitoIdentityId': None, 'caller': None, 'sourceIp': '98.15.66.96', 'principalOrgId': None, 'accessKey': None, 'cognitoAuthenticationType': None, 'cognitoAuthenticationProvider': None, 'userArn': None, 'userAgent': 'Mozilla/5.0 (iPhone; CPU iPhone OS 15_1_1 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/15.1 Mobile/15E148 Safari/604.1', 'user': None}, 'domainName': 'k9wj046mrd.execute-api.us-east-1.amazonaws.com', 'apiId': 'k9wj046mrd'}, 'body': '{"time":"4:30 AM","departure":"Butler","destination":{"address":"8 W","latitude":40.6342596,"longitude":-74.1184507}}', 'isBase64Encoded': False}

    
    token = event['queryStringParameters']['accessToken']
    email = email_from_token(token)
    # email = "yl4735@columbia.edu"
    info = get_trip_info(event)
    
    print(info)
    put_trip(email, info)
    # time.sleep(0.)
    # create_group(email, info)
    print("<<<")
    return {
        'headers': {'Access-Control-Allow-Origin': "*"},
        'statusCode': 200,
        'body': json.dumps('trip post sucess')
    }

