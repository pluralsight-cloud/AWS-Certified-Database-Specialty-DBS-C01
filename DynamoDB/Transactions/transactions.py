import time
import boto3
from botocore.exceptions import ClientError
client = boto3.client("dynamodb")
existing_tables = client.list_tables()["TableNames"]
try:
    print("TransactWriteItems")
    response = client.transact_write_items(
    TransactItems=[
        {
            'Update': {
                'TableName':'movie_ticket',
                'Key': {
                    'movie_ticket_id': { 'N': '28222' },
                    'movie_name': { 'S': 'Cast Away' }
                },
                "UpdateExpression": "set in_stock = in_stock - :decr",
                "ExpressionAttributeValues": {
                        ":decr": {"N": "1"}
                }, 
                "ConditionExpression": "in_stock >= :decr"
            }
        },
        {
            'Put': {
                'TableName': 'order',
                'Item': {
                    'order_id': {'N': '001' },
                    'purchase_time':{'N': str(int(time.time()))}
                }
            }
        }
    ]
)
except ClientError as e:
    print("An error occurred during the transaction:")
    print(f"Error Code: {e.response['Error']['Code']}")
    if 'CancellationReasons' in e.response['Error']:
        print(f"Cancellation Reasons: {e.response['Error']['CancellationReasons']}")
    else:
        print("No Cancellation Reasons provided.")
else:
    print("TransactWriteItems succeeded:")
    print(response)
