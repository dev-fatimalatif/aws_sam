# import json

# # import requests


# def lambda_handler(event, context):
#     """Sample pure Lambda function

#     Parameters
#     ----------
#     event: dict, required
#         API Gateway Lambda Proxy Input Format

#         Event doc: https://docs.aws.amazon.com/apigateway/latest/developerguide/set-up-lambda-proxy-integrations.html#api-gateway-simple-proxy-for-lambda-input-format

#     context: object, required
#         Lambda Context runtime methods and attributes

#         Context doc: https://docs.aws.amazon.com/lambda/latest/dg/python-context-object.html

#     Returns
#     ------
#     API Gateway Lambda Proxy Output Format: dict

#         Return doc: https://docs.aws.amazon.com/apigateway/latest/developerguide/set-up-lambda-proxy-integrations.html
#     """

#     # try:
#     #     ip = requests.get("http://checkip.amazonaws.com/")
#     # except requests.RequestException as e:
#     #     # Send some context about this error to Lambda Logs
#     #     print(e)

#     #     raise e

#     return {
#         "statusCode": 200,
#         "body": json.dumps({
#             "message": "hello world",
#             # "location": ip.text.replace("\n", "")
#         }),
#     }
import json
import boto3
import decimal
from botocore.exceptions import ClientError

# get a list of all movies
def lambda_handler(event, context):
    
    response = get_movies_from_db()

    return {
        'statusCode': 200,
        'body': json.dumps(response, indent=2, default=handle_decimal_type)
    }

# Get a list of all movies from DynamoDB table
def get_movies_from_db():
    
    dynamodb = boto3.resource('dynamodb')
    table = dynamodb.Table('movies-table')

    try:
        response = table.scan()
    except ClientError as e:
        print(e.response['Error']['Message'])
    else:
        return response.get('Items', [])
        
        
# The problem is that the Dynamo Python library is converting numeric values to Decimal objects, 
# but those aren't JSON serializable by default, so json.dumps blows up. 
# You will need to provide json.dumps with a converter for Decimal objects.
def handle_decimal_type(obj):
    if isinstance(obj, decimal.Decimal):
        if float(obj).is_integer():
            return int(obj)
        else:
            return float(obj)
    raise TypeError