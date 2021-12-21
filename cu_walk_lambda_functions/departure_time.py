import json
import boto3
# this lambda takes a access toke, find email, use email find group the user selected, return group info
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
def find_group(email):
    TABLE_NAME = "groups"
    client = boto3.resource('dynamodb')
    table = client.Table(TABLE_NAME)
    response = table.scan()
    groups = response['Items']
    for g in groups:
        teamates = json.loads(g['teamates'])['value']
        if email in teamates:
            print(g)
            return g
    print("no group find")
    return False
def lambda_handler(event, context):
    # TODO implement
    
    print(">>>")
    print(event)
    print("<<<")
    # event = {'resource': '/getdeparturetime', 'path': '/getdeparturetime', 'httpMethod': 'GET', 'headers': {'accept': '*/*', 'accept-encoding': 'gzip, deflate, br', 'accept-language': 'zh-CN,zh;q=0.9', 'content-type': 'application/json', 'Host': 'k9wj046mrd.execute-api.us-east-1.amazonaws.com', 'origin': 'https://6998frontendtest.s3.amazonaws.com', 'referer': 'https://6998frontendtest.s3.amazonaws.com/', 'sec-ch-ua': '" Not A;Brand";v="99", "Chromium";v="96", "Google Chrome";v="96"', 'sec-ch-ua-mobile': '?0', 'sec-ch-ua-platform': '"macOS"', 'sec-fetch-dest': 'empty', 'sec-fetch-mode': 'cors', 'sec-fetch-site': 'cross-site', 'token': 'eyJraWQiOiJ4Zk9sZTU2ZG5kTmNNUXY5eVMyeTAxeFFLM251TXFtakJZQlhmbkJVUFFrPSIsImFsZyI6IlJTMjU2In0.eyJhdF9oYXNoIjoiZFFsWDJZVURNOU0zRTVQbC11SlBlZyIsInN1YiI6IjNlMzEzYWVjLWNkNDUtNDUzOC05YjI4LTUyYWNiYjBhODc0MyIsImNvZ25pdG86Z3JvdXBzIjpbInVzLWVhc3QtMV8wck51b051YzRfR29vZ2xlIl0sImVtYWlsX3ZlcmlmaWVkIjp0cnVlLCJpc3MiOiJodHRwczpcL1wvY29nbml0by1pZHAudXMtZWFzdC0xLmFtYXpvbmF3cy5jb21cL3VzLWVhc3QtMV8wck51b051YzQiLCJjb2duaXRvOnVzZXJuYW1lIjoiZ29vZ2xlXzExMjQ1NjEzMzU4MDU5MjY3MjM4NCIsImF1ZCI6InV1ZG9wNWppNGE5MzBoZDJsZDhnaW80cW4iLCJpZGVudGl0aWVzIjpbeyJ1c2VySWQiOiIxMTI0NTYxMzM1ODA1OTI2NzIzODQiLCJwcm92aWRlck5hbWUiOiJHb29nbGUiLCJwcm92aWRlclR5cGUiOiJHb29nbGUiLCJpc3N1ZXIiOm51bGwsInByaW1hcnkiOiJ0cnVlIiwiZGF0ZUNyZWF0ZWQiOiIxNjM4NTA5NTY2Mzk4In1dLCJ0b2tlbl91c2UiOiJpZCIsImF1dGhfdGltZSI6MTYzOTk2MDUxMywibmFtZSI6IllhbmhhbyBMaSIsImV4cCI6MTYzOTk2NDExMywiaWF0IjoxNjM5OTYwNTEzLCJqdGkiOiIzYmExYTY1Yy05YmYxLTRiMmMtOWY0Zi04MmJiOWQ1N2QyYjYiLCJlbWFpbCI6InlsNDczNUBjb2x1bWJpYS5lZHUifQ.Zfff9GKRjRd_gESnVWAnOaLRexxs53cawdZsXcJhIhm94UfSePQJTs-Bss3ON-g3UwogOvUWmOGfQsshj3aGwxUqoaeDoQYS8EqypODoJZvCkyXrT3fRyfHyfKwR4F_XxU4mTcAWMpGy9hImNyx7_QRDvK7UFB3EmyTR8HJsfvz7CwkWnZDwYRO6FrqeSioDLOY58DTf6XtEjd8b-0OFfV-aQyA4vU5bDR07wAKNmBmrMuNi9Q0e94G7woTqLiEvF6oAa41ltIThCSmxCOa-fEUCZ1klNiATTZZfnouS3dB2T7QnJG3Iq-uP8ZEE3RD6Syfy5y3_AgfdE9ZxfMg2sQ', 'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/96.0.4664.110 Safari/537.36', 'X-Amzn-Trace-Id': 'Root=1-61bfcfd3-6425ac5e74fbd6647518bef1', 'X-Forwarded-For': '98.15.66.96', 'X-Forwarded-Port': '443', 'X-Forwarded-Proto': 'https'}, 'multiValueHeaders': {'accept': ['*/*'], 'accept-encoding': ['gzip, deflate, br'], 'accept-language': ['zh-CN,zh;q=0.9'], 'content-type': ['application/json'], 'Host': ['k9wj046mrd.execute-api.us-east-1.amazonaws.com'], 'origin': ['https://6998frontendtest.s3.amazonaws.com'], 'referer': ['https://6998frontendtest.s3.amazonaws.com/'], 'sec-ch-ua': ['" Not A;Brand";v="99", "Chromium";v="96", "Google Chrome";v="96"'], 'sec-ch-ua-mobile': ['?0'], 'sec-ch-ua-platform': ['"macOS"'], 'sec-fetch-dest': ['empty'], 'sec-fetch-mode': ['cors'], 'sec-fetch-site': ['cross-site'], 'token': ['eyJraWQiOiJ4Zk9sZTU2ZG5kTmNNUXY5eVMyeTAxeFFLM251TXFtakJZQlhmbkJVUFFrPSIsImFsZyI6IlJTMjU2In0.eyJhdF9oYXNoIjoiZFFsWDJZVURNOU0zRTVQbC11SlBlZyIsInN1YiI6IjNlMzEzYWVjLWNkNDUtNDUzOC05YjI4LTUyYWNiYjBhODc0MyIsImNvZ25pdG86Z3JvdXBzIjpbInVzLWVhc3QtMV8wck51b051YzRfR29vZ2xlIl0sImVtYWlsX3ZlcmlmaWVkIjp0cnVlLCJpc3MiOiJodHRwczpcL1wvY29nbml0by1pZHAudXMtZWFzdC0xLmFtYXpvbmF3cy5jb21cL3VzLWVhc3QtMV8wck51b051YzQiLCJjb2duaXRvOnVzZXJuYW1lIjoiZ29vZ2xlXzExMjQ1NjEzMzU4MDU5MjY3MjM4NCIsImF1ZCI6InV1ZG9wNWppNGE5MzBoZDJsZDhnaW80cW4iLCJpZGVudGl0aWVzIjpbeyJ1c2VySWQiOiIxMTI0NTYxMzM1ODA1OTI2NzIzODQiLCJwcm92aWRlck5hbWUiOiJHb29nbGUiLCJwcm92aWRlclR5cGUiOiJHb29nbGUiLCJpc3N1ZXIiOm51bGwsInByaW1hcnkiOiJ0cnVlIiwiZGF0ZUNyZWF0ZWQiOiIxNjM4NTA5NTY2Mzk4In1dLCJ0b2tlbl91c2UiOiJpZCIsImF1dGhfdGltZSI6MTYzOTk2MDUxMywibmFtZSI6IllhbmhhbyBMaSIsImV4cCI6MTYzOTk2NDExMywiaWF0IjoxNjM5OTYwNTEzLCJqdGkiOiIzYmExYTY1Yy05YmYxLTRiMmMtOWY0Zi04MmJiOWQ1N2QyYjYiLCJlbWFpbCI6InlsNDczNUBjb2x1bWJpYS5lZHUifQ.Zfff9GKRjRd_gESnVWAnOaLRexxs53cawdZsXcJhIhm94UfSePQJTs-Bss3ON-g3UwogOvUWmOGfQsshj3aGwxUqoaeDoQYS8EqypODoJZvCkyXrT3fRyfHyfKwR4F_XxU4mTcAWMpGy9hImNyx7_QRDvK7UFB3EmyTR8HJsfvz7CwkWnZDwYRO6FrqeSioDLOY58DTf6XtEjd8b-0OFfV-aQyA4vU5bDR07wAKNmBmrMuNi9Q0e94G7woTqLiEvF6oAa41ltIThCSmxCOa-fEUCZ1klNiATTZZfnouS3dB2T7QnJG3Iq-uP8ZEE3RD6Syfy5y3_AgfdE9ZxfMg2sQ'], 'User-Agent': ['Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/96.0.4664.110 Safari/537.36'], 'X-Amzn-Trace-Id': ['Root=1-61bfcfd3-6425ac5e74fbd6647518bef1'], 'X-Forwarded-For': ['98.15.66.96'], 'X-Forwarded-Port': ['443'], 'X-Forwarded-Proto': ['https']}, 'queryStringParameters': {'_': '1639960530923', 'accessToken': 'eyJraWQiOiI4UkY1TDZtdEhGQlBFRkNaSFFPeGxFY2p6azVIVGNaQWZ6a1lLUG9LS3VzPSIsImFsZyI6IlJTMjU2In0.eyJzdWIiOiIzZTMxM2FlYy1jZDQ1LTQ1MzgtOWIyOC01MmFjYmIwYTg3NDMiLCJjb2duaXRvOmdyb3VwcyI6WyJ1cy1lYXN0LTFfMHJOdW9OdWM0X0dvb2dsZSJdLCJ0b2tlbl91c2UiOiJhY2Nlc3MiLCJzY29wZSI6ImF3cy5jb2duaXRvLnNpZ25pbi51c2VyLmFkbWluIHBob25lIG9wZW5pZCBwcm9maWxlIGVtYWlsIiwiYXV0aF90aW1lIjoxNjM5OTYwNTEzLCJpc3MiOiJodHRwczpcL1wvY29nbml0by1pZHAudXMtZWFzdC0xLmFtYXpvbmF3cy5jb21cL3VzLWVhc3QtMV8wck51b051YzQiLCJleHAiOjE2Mzk5NjQxMTMsImlhdCI6MTYzOTk2MDUxMywidmVyc2lvbiI6MiwianRpIjoiNmIzZTYzZjEtNTk2Ni00OGIxLTljZGQtNmE5NTI5YjIyZjI4IiwiY2xpZW50X2lkIjoidXVkb3A1amk0YTkzMGhkMmxkOGdpbzRxbiIsInVzZXJuYW1lIjoiZ29vZ2xlXzExMjQ1NjEzMzU4MDU5MjY3MjM4NCJ9.iox14Xu6zeVZZhE9Qsgynls8XI832UXzhh_EuWXTusgZc0DPv_c1GCPLUzUVUjSlG_vBwPbm2-NcF3XqieI7Ip6rkVAX5m58vT-7o3h3o-HGwmbA9bfXH0F3Ylb0KHOI3k6-QnuksjCWQJcwoxvT03rzR_ZROYp7z2eb19SBqCH6TxL_4UZIqOD89-TI8rKmEGxtBMJehljCvhwerPHwHsI1WbHJ7iMatyig_hGiMPKn6DR_G--rPE29TVJMXS4kjAQZbRkESsKtT49v19WEwntlqQit4AYkZp8AyulpMNBWmC3qAxI_cfzc3jbVqbqOgZUZod92bwMTtx5-gc_bkw'}, 'multiValueQueryStringParameters': {'_': ['1639960530923'], 'accessToken': ['eyJraWQiOiI4UkY1TDZtdEhGQlBFRkNaSFFPeGxFY2p6azVIVGNaQWZ6a1lLUG9LS3VzPSIsImFsZyI6IlJTMjU2In0.eyJzdWIiOiIzZTMxM2FlYy1jZDQ1LTQ1MzgtOWIyOC01MmFjYmIwYTg3NDMiLCJjb2duaXRvOmdyb3VwcyI6WyJ1cy1lYXN0LTFfMHJOdW9OdWM0X0dvb2dsZSJdLCJ0b2tlbl91c2UiOiJhY2Nlc3MiLCJzY29wZSI6ImF3cy5jb2duaXRvLnNpZ25pbi51c2VyLmFkbWluIHBob25lIG9wZW5pZCBwcm9maWxlIGVtYWlsIiwiYXV0aF90aW1lIjoxNjM5OTYwNTEzLCJpc3MiOiJodHRwczpcL1wvY29nbml0by1pZHAudXMtZWFzdC0xLmFtYXpvbmF3cy5jb21cL3VzLWVhc3QtMV8wck51b051YzQiLCJleHAiOjE2Mzk5NjQxMTMsImlhdCI6MTYzOTk2MDUxMywidmVyc2lvbiI6MiwianRpIjoiNmIzZTYzZjEtNTk2Ni00OGIxLTljZGQtNmE5NTI5YjIyZjI4IiwiY2xpZW50X2lkIjoidXVkb3A1amk0YTkzMGhkMmxkOGdpbzRxbiIsInVzZXJuYW1lIjoiZ29vZ2xlXzExMjQ1NjEzMzU4MDU5MjY3MjM4NCJ9.iox14Xu6zeVZZhE9Qsgynls8XI832UXzhh_EuWXTusgZc0DPv_c1GCPLUzUVUjSlG_vBwPbm2-NcF3XqieI7Ip6rkVAX5m58vT-7o3h3o-HGwmbA9bfXH0F3Ylb0KHOI3k6-QnuksjCWQJcwoxvT03rzR_ZROYp7z2eb19SBqCH6TxL_4UZIqOD89-TI8rKmEGxtBMJehljCvhwerPHwHsI1WbHJ7iMatyig_hGiMPKn6DR_G--rPE29TVJMXS4kjAQZbRkESsKtT49v19WEwntlqQit4AYkZp8AyulpMNBWmC3qAxI_cfzc3jbVqbqOgZUZod92bwMTtx5-gc_bkw']}, 'pathParameters': None, 'stageVariables': None, 'requestContext': {'resourceId': 'ctbisj', 'resourcePath': '/getdeparturetime', 'httpMethod': 'GET', 'extendedRequestId': 'Kn1pAGfXoAMFrHg=', 'requestTime': '20/Dec/2021:00:35:31 +0000', 'path': '/6998FirstTry/getdeparturetime', 'accountId': '680019774401', 'protocol': 'HTTP/1.1', 'stage': '6998FirstTry', 'domainPrefix': 'k9wj046mrd', 'requestTimeEpoch': 1639960531048, 'requestId': '964d4b28-883a-4591-9f4b-122ee7d9a187', 'identity': {'cognitoIdentityPoolId': None, 'accountId': None, 'cognitoIdentityId': None, 'caller': None, 'sourceIp': '98.15.66.96', 'principalOrgId': None, 'accessKey': None, 'cognitoAuthenticationType': None, 'cognitoAuthenticationProvider': None, 'userArn': None, 'userAgent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/96.0.4664.110 Safari/537.36', 'user': None}, 'domainName': 'k9wj046mrd.execute-api.us-east-1.amazonaws.com', 'apiId': 'k9wj046mrd'}, 'body': None, 'isBase64Encoded': False}

    email = email_from_token(event)
    print(email)
    # email = "yl4735@columbia.edu"
    group = find_group(email)
    print(group)
    return {
        'headers': {'Access-Control-Allow-Origin': "*"},
        'statusCode': 200,
        'body': json.dumps(group)
    }
