import json
from .response import get_response

def lambda_handler(event, context):

    return {
        "statusCode": 200,
        "body": json.dumps(get_response()),
    }