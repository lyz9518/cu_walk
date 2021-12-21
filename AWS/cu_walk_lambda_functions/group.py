import json
import boto3
import googlemaps
from boto3.dynamodb.conditions import Attr
import ast
import time
import random
# After user submit their trip info, they will be directed to select group page, the get method provides satisfied groups info
# Get method takes an access toke to find email, then find user's trip info from individualtrip DB.
# return satisfied groups based on trip info

# Post method takes id_token, first_user_coordinate, time, then find the gourp with first_user_coordinate, add email to teamates, delete unused group
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

    

def find_trip(email):
    client = boto3.client('dynamodb')
    response = client.get_item(
            TableName='individual_trip',
            Key={
                'email': {
                    'S': email
                }
            }
        )
    raw = response['Item']
    print("trip info!!!!")
    print(raw)
    info = {
        'time': raw['time']['S'],
        'departure': raw['departure']['S'],
        'destination': json.loads(raw['destination']['S']),
        'code': raw['departure']['S']
    }
    return info

def find_satisfied_groups(email, info):
    # group DB attributes: time, departure, teamates, first_user_coordinate
    # the function will find a group first based on time  then makes sure the existing group destination is within 800m
    
    # get the list of groups with same time
    TABLE_NAME = "groups"
    time = info['time']
    client = boto3.resource('dynamodb')
    table = client.Table(TABLE_NAME)
    response = table.scan(
        FilterExpression=Attr('time').eq(time)
        )
    
    groups = response['Items']
    print(response['Items'])
    satisfied_groups = []
    for group in groups:
        distance = calculate_distance(group["first_user_coordinate"], info["destination"])
        if distance < 200 and time == group["time"]:
            satisfied_groups.append(group)
    return satisfied_groups
    
def get_groupkey(event, info):
    body = event['body']
    body = ast.literal_eval(body)
    key = {
        "first_user_coordinate": body['first_user_coordinate'],
        "time": info["time"]
    }
    return key
    
def get_flag(event):
    body = event['body']
    print(body)
    body = ast.literal_eval(body)
    return body["create_new_group"]

def insert_to_group(email, group_key, user_destination):
    # find the group by first_user_coordinate, which is partition key of group DB
    
    client = boto3.client('dynamodb')
    response = client.get_item(
            TableName='groups',
            Key={
                'first_user_coordinate': {
                    'S': group_key['first_user_coordinate']
                },
                'time': {
                    'S': group_key['time']
                }    
                
            }
        )
    
    # print(response)
    if 'Item' in response.keys():
        raw = response['Item']
        selected_group_info = format_raw(raw)
        # if info['team_size'] == 0 and info['first_user_coordinate'] == user_destination:
        #     # selected inialize group
        print("find group info:")
        # if int(selected_group_info['team_size']) != 0 or selected_group_info['first_user_coordinate'] != user_destination:
        #     # selected non-initialize group, need to delete initialized group if team size is 0
        #     delete_initial_group(user_destination, group_key['time'])
            
        print("group INFO!!!")
        print(selected_group_info)
        # get group info by get_item, then delete it
        # add to teamates list
        selected_group_info['teamates'].append(email)
        client = boto3.client('dynamodb')
        teamates = json.dumps({'value': selected_group_info['teamates']})
        # put new group info to group DB
        response = client.put_item(
            TableName='groups',
            Item={
                'first_user_coordinate': {'S': json.dumps(selected_group_info['first_user_coordinate'])},
                'time': {'S': selected_group_info['time']},
                'departure': {'S': selected_group_info['departure']},
                'teamates': {'S': teamates},
                'code': {'S': selected_group_info['code']}
            }
        )
    print(response)
    return 'group not exist'

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
    print(result["rows"][0]["elements"])
    print("!!!!!!!!!!!!!!")
    return result["rows"][0]["elements"][0]["distance"]["value"]

def delete_initial_group(user_destination, time):
    # need to modify for considering before user selecting non-intial group, other user joined this group
    client = boto3.client('dynamodb')
    response = client.delete_item(
        TableName='groups',
        Key={
            'first_user_coordinate': {
                'S': user_destination
            },
            'time': {
                'S': time
            }
        }
    )
    print("deleted initial ")
    return response
def format_raw(raw):
    info = {
            'first_user_coordinate': json.loads(raw['first_user_coordinate']['S']),
            'teamates': json.loads(raw['teamates']['S'])['value'],
            'time': raw['time']['S'],
            'departure': raw['departure']['S'],
            'team_size': len(json.loads(raw['teamates']['S'])['value']),
            'code': raw['code']['S']
        }
    return info
def pop_by_key(key):
     # get group info by get_item, then delete it
    client = boto3.client('dynamodb')
    r1 = client.get_item(
        TableName='groups',
        Key={
            'first_user_coordinate': {
                'S': key
            }
        }
    )
    res = format_raw(r1['Item'])
    response = client.delete_item(
        TableName='groups',
        Key={
            'first_user_coordinate': {
                'S': key
            }
        }
    )
    return res
    
def create_group(email, info):
    # create an empty group with user info
    code = random.randint(1000,9999)
    client = boto3.client('dynamodb')
    teamates = json.dumps({'value': [email]})
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

def lambda_handler(event, context):
    
    print(">>>")
    print(event)
    print("<<<")
    
    method = event['httpMethod']
    if method == "GET":
        time.sleep(1)
        # email = "yl4735@columbia.edu"
        email = email_from_token(event) 
        trip_info = find_trip(email)
        print(trip_info)
        groups = find_satisfied_groups(email, trip_info)
        # print(groups)
        for g in groups:
            g['team_size'] = int(len(json.loads(g['teamates'])['value'])) # convert to int because json does not accept decimal type
        print(groups)
        return {
            'headers': {'Access-Control-Allow-Origin': "*"},
            'statusCode': 200,
            'body': json.dumps(groups)
        }
    if method == "POST":
        flag = get_flag(event)
        email = email_from_token(event) 
        trip_info = find_trip(email)
        user_destination = json.dumps(trip_info['destination'])
        if flag == "JOIN":
            group_key = get_groupkey(event, trip_info) # use first_user_coordinate and time as key
            # group_key = {
            #     "first_user_coordinate": user_destination,
            #     "time": trip_info["time"]
            # }
            
            insert_to_group(email, group_key, user_destination)
            return {
                'headers': {'Access-Control-Allow-Origin': "*"},
                'statusCode': 200,
                'body': json.dumps('insert to group success')
            }
        if flag == "CREATE":
            create_group(email, trip_info)
            return {
                'headers': {'Access-Control-Allow-Origin': "*"},
                'statusCode': 200,
                'body': json.dumps('create group success')
            }
            
    return {
            'headers': {'Access-Control-Allow-Origin': "*"},
            'statusCode': 200,
            'body': json.dumps("wrong meth")
        }
