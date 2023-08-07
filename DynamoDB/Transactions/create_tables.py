#!/usr/bin/env python3
import boto3
from botocore.exceptions import ClientError
client = boto3.client("dynamodb")
existing_tables = client.list_tables()["TableNames"]
if "order" not in existing_tables:
    print("Creating order table")
    response = client.create_table(
        TableName="order",
        KeySchema=[
            {"AttributeName": "order_id", "KeyType": "HASH"},
            {"AttributeName": "purchase_time", "KeyType": "RANGE"},
        ],
        AttributeDefinitions=[
            {"AttributeName": "order_id", "AttributeType": "N"},
           {"AttributeName": "purchase_time", "AttributeType": "N"},

        ],
        BillingMode="PAY_PER_REQUEST",
    )
    print(f"Waiting for table order...")
    waiter = client.get_waiter("table_exists")
    waiter.wait(TableName="order")
    
if "movie_ticket" not in existing_tables:
    print("Creating movie_ticket table")
    response = client.create_table(
        TableName="movie_ticket",
        KeySchema=[
            {"AttributeName": "movie_ticket_id", "KeyType": "HASH"},
            {"AttributeName": "movie_name", "KeyType": "RANGE"},
        ],
        AttributeDefinitions=[
            {"AttributeName": "movie_ticket_id", "AttributeType": "N"},
            {"AttributeName": "movie_name", "AttributeType": "S"},
        ],
        BillingMode="PAY_PER_REQUEST",
    )
    print(f"Waiting for table movie_ticket...")
    waiter = client.get_waiter("table_exists")
    waiter.wait(TableName="movie_ticket")
    
# After both tables have been created and are active, proceed to populate the "movie_ticket" table.
response = client.put_item(
    TableName="movie_ticket",
    Item={
        "movie_ticket_id": {"N": "28222"},
        "movie_name": {"S": "Cast Away"},
        "in_stock": {"N": "55"}
    }
)
print(f"Populating the movie ticket table...")
print(response)
