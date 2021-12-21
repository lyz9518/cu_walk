import json

# https://docs.aws.amazon.com/cognito/latest/developerguide/user-pool-lambda-pre-authentication.html
def lambda_handler(event, context):
    print(event)
    email = event['request']['userAttributes']['email']
    email_org = email.split("@")[1]
    if email_org != "columbia.edu":
        raise Exception("Please_use_Email_of_Columbia_University_to_log_in")
        # raise Exception("Cannot authenticate users from this user pool app client")
    # Return to Amazon Cognito
    return event