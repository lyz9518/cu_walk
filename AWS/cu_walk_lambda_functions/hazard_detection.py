# this lambda is used for hazard detection
# it takes user current coordinate and trip direction( a list of coordinates) 

import googlemaps
import json
import ast
def get_info(event):
    body = ast.literal_eval(event['body'])
    direction = body['pointsArray']
    user_coordinate = body['curLocation']
    return user_coordinate, direction

def calculate_distance(origin, destination):
    API_key = "AIzaSyDrVTUpcyFC5ZdYLszLJNe4wB17g_dAc4A"
    gmaps = googlemaps.Client(key=API_key)
    origin = (origin['lat'], origin['lng'])
    result = gmaps.distance_matrix(origin, destination, mode='walking')
    d = result["rows"][0]["elements"][0]
    if 'status' in d.keys() and d['status'] == 'ZERO_RESULTS':
        print('invalid address')
        return 60000
    return result["rows"][0]["elements"][0]["distance"]["value"]

# def update_group_direction(first_user_coordinate, time, direction):
#     TABLE_NAME = "groups"
#     client = boto3.resource('dynamodb')
#     table = client.Table(TABLE_NAME)
#     response = table.update_item(
#                     TableName='groups',
#                     Key={
#                         'first_user_coordinate': first_user_coordinate,
#                         'time': time
#                     }
#                     AttributeUpdates={
#                         'direction': direction
#                         }
#                 )

def check_on_trip(user_coordinate, direction):
    for i in range(0, len(direction), 2):
        trip_coor=direction[i]
        trip_coor = (trip_coor[0],trip_coor[1])
        print(trip_coor)
        distance = calculate_distance(user_coordinate, trip_coor)
        print("distance", distance)
        if distance < 500:
            return "safe"
    return "off"

def lambda_handler(event, context):
    print(">>>")
    print(event)
    print("<<<")
    # event = {'resource': '/hazard_detection', 'path': '/hazard_detection', 'httpMethod': 'POST', 'headers': {'accept': '*/*', 'accept-encoding': 'gzip, deflate, br', 'accept-language': 'zh-CN,zh;q=0.9', 'content-type': 'application/json', 'Host': 'k9wj046mrd.execute-api.us-east-1.amazonaws.com', 'origin': 'https://6998frontendtest.s3.amazonaws.com', 'referer': 'https://6998frontendtest.s3.amazonaws.com/', 'sec-ch-ua': '" Not A;Brand";v="99", "Chromium";v="96", "Google Chrome";v="96"', 'sec-ch-ua-mobile': '?0', 'sec-ch-ua-platform': '"macOS"', 'sec-fetch-dest': 'empty', 'sec-fetch-mode': 'cors', 'sec-fetch-site': 'cross-site', 'token': 'eyJraWQiOiJ4Zk9sZTU2ZG5kTmNNUXY5eVMyeTAxeFFLM251TXFtakJZQlhmbkJVUFFrPSIsImFsZyI6IlJTMjU2In0.eyJhdF9oYXNoIjoiR0JuQzRNWndVMlo4OG1TeHM5UER0ZyIsInN1YiI6IjNlMzEzYWVjLWNkNDUtNDUzOC05YjI4LTUyYWNiYjBhODc0MyIsImNvZ25pdG86Z3JvdXBzIjpbInVzLWVhc3QtMV8wck51b051YzRfR29vZ2xlIl0sImVtYWlsX3ZlcmlmaWVkIjp0cnVlLCJpc3MiOiJodHRwczpcL1wvY29nbml0by1pZHAudXMtZWFzdC0xLmFtYXpvbmF3cy5jb21cL3VzLWVhc3QtMV8wck51b051YzQiLCJjb2duaXRvOnVzZXJuYW1lIjoiZ29vZ2xlXzExMjQ1NjEzMzU4MDU5MjY3MjM4NCIsIm5vbmNlIjoiQ2dhUXdlenFWZ2Ftb3VvUEp5V2IxOW00dGc1dUV1STYwaTl6bkRDVXhhbE5FN3daaUVzbE1TR3BNSzI5dE9WdklwT01yV3B2V3JaX1ZQT2pPN2U5R21qRlktaUl2dEtjalhXTXFCMFBpZ0U5MG4yR0lhZ0dhcVU3Yjg0ek9UdjVIOXA5NGlNUDhYZUt3MnJOVGRKQTE3Qlo1alNfUnk3dTRyeXFFRGNfQWtzIiwiYXVkIjoidXVkb3A1amk0YTkzMGhkMmxkOGdpbzRxbiIsImlkZW50aXRpZXMiOlt7InVzZXJJZCI6IjExMjQ1NjEzMzU4MDU5MjY3MjM4NCIsInByb3ZpZGVyTmFtZSI6Ikdvb2dsZSIsInByb3ZpZGVyVHlwZSI6Ikdvb2dsZSIsImlzc3VlciI6bnVsbCwicHJpbWFyeSI6InRydWUiLCJkYXRlQ3JlYXRlZCI6IjE2Mzg1MDk1NjYzOTgifV0sInRva2VuX3VzZSI6ImlkIiwiYXV0aF90aW1lIjoxNjM5OTU5NDQ2LCJuYW1lIjoiWWFuaGFvIExpIiwiZXhwIjoxNjM5OTYzMDQ2LCJpYXQiOjE2Mzk5NTk0NDYsImp0aSI6ImI0N2M1ZjhjLWJkMzctNGU2Yy1hYjk1LTc4MGE4NzFkYTQ3MyIsImVtYWlsIjoieWw0NzM1QGNvbHVtYmlhLmVkdSJ9.geeZSEBC4ay72W2JtQRO-YrqY8Qh_JpjKjdCURPm3yazqNOiL008rXOgd12cpktoONSwPu96N57AHKW2D6VVB1HNkgkbAcZgM-i1gqj7d9y9-YDBpNdmNyMNMY3_a5zeV_ZSpwSEIc9giwsP9q2RhGTIUY81CiPhrZBaYz4q1jVG7IN_YpO-PFpd7yeGNuyxDEXBpgm3is_bRAsK3G0jF0LOZwNKiJzN1_6T4ujCcMwLvHwY7GINIrBQ3TLwephYMK9zV_5Il70Tutq1o6yPczYKl8tGp6OoNorTLYkhU7q4QDjCvQ5ZXVvhgRIf5P_1wcraKMSqKTClZoSb5UraTA', 'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/96.0.4664.110 Safari/537.36', 'X-Amzn-Trace-Id': 'Root=1-61bfcdf1-014a52c4488b489262373cb3', 'X-Forwarded-For': '98.15.66.96', 'X-Forwarded-Port': '443', 'X-Forwarded-Proto': 'https'}, 'multiValueHeaders': {'accept': ['*/*'], 'accept-encoding': ['gzip, deflate, br'], 'accept-language': ['zh-CN,zh;q=0.9'], 'content-type': ['application/json'], 'Host': ['k9wj046mrd.execute-api.us-east-1.amazonaws.com'], 'origin': ['https://6998frontendtest.s3.amazonaws.com'], 'referer': ['https://6998frontendtest.s3.amazonaws.com/'], 'sec-ch-ua': ['" Not A;Brand";v="99", "Chromium";v="96", "Google Chrome";v="96"'], 'sec-ch-ua-mobile': ['?0'], 'sec-ch-ua-platform': ['"macOS"'], 'sec-fetch-dest': ['empty'], 'sec-fetch-mode': ['cors'], 'sec-fetch-site': ['cross-site'], 'token': ['eyJraWQiOiJ4Zk9sZTU2ZG5kTmNNUXY5eVMyeTAxeFFLM251TXFtakJZQlhmbkJVUFFrPSIsImFsZyI6IlJTMjU2In0.eyJhdF9oYXNoIjoiR0JuQzRNWndVMlo4OG1TeHM5UER0ZyIsInN1YiI6IjNlMzEzYWVjLWNkNDUtNDUzOC05YjI4LTUyYWNiYjBhODc0MyIsImNvZ25pdG86Z3JvdXBzIjpbInVzLWVhc3QtMV8wck51b051YzRfR29vZ2xlIl0sImVtYWlsX3ZlcmlmaWVkIjp0cnVlLCJpc3MiOiJodHRwczpcL1wvY29nbml0by1pZHAudXMtZWFzdC0xLmFtYXpvbmF3cy5jb21cL3VzLWVhc3QtMV8wck51b051YzQiLCJjb2duaXRvOnVzZXJuYW1lIjoiZ29vZ2xlXzExMjQ1NjEzMzU4MDU5MjY3MjM4NCIsIm5vbmNlIjoiQ2dhUXdlenFWZ2Ftb3VvUEp5V2IxOW00dGc1dUV1STYwaTl6bkRDVXhhbE5FN3daaUVzbE1TR3BNSzI5dE9WdklwT01yV3B2V3JaX1ZQT2pPN2U5R21qRlktaUl2dEtjalhXTXFCMFBpZ0U5MG4yR0lhZ0dhcVU3Yjg0ek9UdjVIOXA5NGlNUDhYZUt3MnJOVGRKQTE3Qlo1alNfUnk3dTRyeXFFRGNfQWtzIiwiYXVkIjoidXVkb3A1amk0YTkzMGhkMmxkOGdpbzRxbiIsImlkZW50aXRpZXMiOlt7InVzZXJJZCI6IjExMjQ1NjEzMzU4MDU5MjY3MjM4NCIsInByb3ZpZGVyTmFtZSI6Ikdvb2dsZSIsInByb3ZpZGVyVHlwZSI6Ikdvb2dsZSIsImlzc3VlciI6bnVsbCwicHJpbWFyeSI6InRydWUiLCJkYXRlQ3JlYXRlZCI6IjE2Mzg1MDk1NjYzOTgifV0sInRva2VuX3VzZSI6ImlkIiwiYXV0aF90aW1lIjoxNjM5OTU5NDQ2LCJuYW1lIjoiWWFuaGFvIExpIiwiZXhwIjoxNjM5OTYzMDQ2LCJpYXQiOjE2Mzk5NTk0NDYsImp0aSI6ImI0N2M1ZjhjLWJkMzctNGU2Yy1hYjk1LTc4MGE4NzFkYTQ3MyIsImVtYWlsIjoieWw0NzM1QGNvbHVtYmlhLmVkdSJ9.geeZSEBC4ay72W2JtQRO-YrqY8Qh_JpjKjdCURPm3yazqNOiL008rXOgd12cpktoONSwPu96N57AHKW2D6VVB1HNkgkbAcZgM-i1gqj7d9y9-YDBpNdmNyMNMY3_a5zeV_ZSpwSEIc9giwsP9q2RhGTIUY81CiPhrZBaYz4q1jVG7IN_YpO-PFpd7yeGNuyxDEXBpgm3is_bRAsK3G0jF0LOZwNKiJzN1_6T4ujCcMwLvHwY7GINIrBQ3TLwephYMK9zV_5Il70Tutq1o6yPczYKl8tGp6OoNorTLYkhU7q4QDjCvQ5ZXVvhgRIf5P_1wcraKMSqKTClZoSb5UraTA'], 'User-Agent': ['Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/96.0.4664.110 Safari/537.36'], 'X-Amzn-Trace-Id': ['Root=1-61bfcdf1-014a52c4488b489262373cb3'], 'X-Forwarded-For': ['98.15.66.96'], 'X-Forwarded-Port': ['443'], 'X-Forwarded-Proto': ['https']}, 'queryStringParameters': None, 'multiValueQueryStringParameters': None, 'pathParameters': None, 'stageVariables': None, 'requestContext': {'resourceId': 'clmblu', 'resourcePath': '/hazard_detection', 'httpMethod': 'POST', 'extendedRequestId': 'Kn0dyFB7oAMFTsQ=', 'requestTime': '20/Dec/2021:00:27:29 +0000', 'path': '/6998FirstTry/hazard_detection', 'accountId': '680019774401', 'protocol': 'HTTP/1.1', 'stage': '6998FirstTry', 'domainPrefix': 'k9wj046mrd', 'requestTimeEpoch': 1639960049682, 'requestId': '2d5a67a8-dacd-4bc8-b778-b99802d97d40', 'identity': {'cognitoIdentityPoolId': None, 'accountId': None, 'cognitoIdentityId': None, 'caller': None, 'sourceIp': '98.15.66.96', 'principalOrgId': None, 'accessKey': None, 'cognitoAuthenticationType': None, 'cognitoAuthenticationProvider': None, 'userArn': None, 'userAgent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/96.0.4664.110 Safari/537.36', 'user': None}, 'domainName': 'k9wj046mrd.execute-api.us-east-1.amazonaws.com', 'apiId': 'k9wj046mrd'}, 'body': '{"pointsArray":[[40.80979000000001,-73.96071],[40.809670000000004,-73.96043],[40.809650000000005,-73.96043],[40.809520000000006,-73.96051],[40.809470000000005,-73.96050000000001],[40.80932000000001,-73.9606],[40.80932000000001,-73.96062],[40.809250000000006,-73.96066],[40.80923000000001,-73.96065],[40.809200000000004,-73.96059000000001],[40.80877,-73.96086000000001],[40.80875,-73.96084],[40.80854,-73.96099000000001],[40.80854,-73.96100000000001],[40.80856,-73.96105],[40.80838000000001,-73.96118000000001],[40.808170000000004,-73.96133],[40.80809,-73.96113000000001],[40.80798,-73.96122000000001],[40.807860000000005,-73.96130000000001],[40.807700000000004,-73.96094000000001],[40.807590000000005,-73.96066],[40.807550000000006,-73.96064000000001],[40.80754,-73.96063000000001],[40.807430000000004,-73.96037000000001],[40.80715,-73.95974000000001],[40.80715,-73.95969000000001],[40.807100000000005,-73.95971],[40.807100000000005,-73.95975],[40.80709,-73.95976],[40.807080000000006,-73.95978000000001],[40.806560000000005,-73.96015000000001],[40.80624,-73.9594],[40.806160000000006,-73.95922],[40.806070000000005,-73.95928],[40.80574,-73.95953],[40.805490000000006,-73.95971],[40.805420000000005,-73.95974000000001],[40.80416,-73.96016],[40.80359,-73.96037000000001],[40.80201,-73.96090000000001],[40.801950000000005,-73.96092],[40.801880000000004,-73.96094000000001],[40.80171,-73.96092],[40.801410000000004,-73.96112000000001],[40.801280000000006,-73.96122000000001],[40.801050000000004,-73.96139000000001],[40.80044,-73.96184000000001],[40.799870000000006,-73.96049000000001]],"curLocation":{"lat":40.7996945,"lng":-73.9598643}}', 'isBase64Encoded': False}
    
    user_coordinate, direction = get_info(event)
    print(user_coordinate)
    
    # print(direction)
    condition = check_on_trip(user_coordinate, direction)
    result_dict = {'condition': condition}
    
    
    
    return {
        'headers': {'Access-Control-Allow-Origin': "*"},
        'statusCode': 200,
        'body': json.dumps(result_dict)
    }
