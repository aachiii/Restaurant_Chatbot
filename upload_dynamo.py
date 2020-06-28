import os, json, csv, yaml, time
from tqdm import tqdm

# For Database
import boto3




dynamodb = boto3.resource('dynamodb')
# client = boto3.client('dynamodb')
table = dynamodb.create_table(
    TableName='yelp-restaurants',
    KeySchema=[
        {
            'AttributeName': 'Business_ID', #Partition key
            'KeyType': 'HASH'
        },
        {
            'AttributeName': 'insertedAtTimestamp', #sort key
            'KeyType': 'RANGE'
        }
    ],
    AttributeDefinitions=[
        {
            'AttributeName': 'Business_ID',
            'AttributeType': 'S'
        },
        {
            'AttributeName': 'insertedAtTimestamp',
            'AttributeType': 'S'
        },
    ],
    ProvisionedThroughput={
        'ReadCapacityUnits': 5,
        'WriteCapacityUnits': 5
    }
)
# Wait until the table exists.
table.meta.client.get_waiter('table_exists').wait(TableName='yelp-restaurants')

# Print out some data about the table.
print(table.item_count)

import time

with table.batch_writer() as batch:
    with open('yelpdata.csv') as csvfile:
        reader = csv.reader(csvfile)
        #['Business_ID', 'Name', 'Address', 'Coordinates', 'Num_of_Reviews', 'Rating', 'Zip_Code', 'Cuisine']
        for row in reader:
            try:
                batch.put_item(
                Item={
                    'insertedAtTimestamp': time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()),
                    'cuisine': row[7],
                    'Business_ID': row[0],
                    'Name': row[1],
                    'Address': row[2],
                    'Coordinates': row[3],
                    'Num_of_Reviews':row[4],
                    'Rating':row[5],
                    'Zip_Code':row[6]
                })
            except:
                print(row)

from boto3.dynamodb.conditions import Key, Attr

response = table.scan(
    FilterExpression=Attr('cuisine').lt('chinese')
)
items = response['Items']
print(len(items))






























# table = dynamodb.create_table(
#     TableName='staff',
#     KeySchema=[
#         {
#             'AttributeName': 'username',
#             'KeyType': 'HASH'
#         },
#         {
#             'AttributeName': 'last_name',
#             'KeyType': 'RANGE'
#         }
#     ],
#     AttributeDefinitions=[
#         {
#             'AttributeName': 'username',
#             'AttributeType': 'S'
#         },
#         {
#             'AttributeName': 'last_name',
#             'AttributeType': 'S'
#         },
#     ],
#     ProvisionedThroughput={
#         'ReadCapacityUnits': 1,
#         'WriteCapacityUnits': 1
#     }
# )

# table = dynamodb.Table('staff')

# table.put_item(
#    Item={
#         'username': 'ruanb',
#         'first_name': 'ruan',
#         'last_name': 'bekker',
#         'age': 30,
#         'account_type': 'administrator',
#     }
# )
# response = table.get_item(
#    Key={
#         'username': 'ruanb',
#         'last_name': 'bekker'
#     }
# )
# item = response['Item']
# name = item['first_name']
# print(item)
# print("Hello, {}" .format(name))

# print(table.item_count)
# print('-------------')
# print(dynamodb)
# print('-------------')
# # Instantiate a table resource object without actually
# # creating a DynamoDB table. Note that the attributes of this table
# # are lazy-loaded: a request is not made nor are the attribute
# # values populated until the attributes
# # on the table resource are accessed or its load() method is called.
# table = dynamodb.Table('yelp_restaurants')
# # table2 = dynamodb.Table('yelp_restaurantsss')
# print('-------------')
# print(table)
# print('-------------')
# # Header
# header = []



# # Open CSV
# with open('scraped_yelp_results_for_Manhattan.csv') as csvfile:
#     reader = csv.reader(csvfile,delimiter=',')

#     # Parse Each Line
#     with table.batch_writer() as batch:
#         for index,row in enumerate(tqdm(reader)):
#             print('111111')
#             if index == 0:
#                 #save the header to be used as the keys
#                 header = row
#             else:

#                 if row == "":
#                     continue

#                 # Create JSON Object
#                 # Push to DynamoDB

#                 data = {}

#                 # Iterate over each column
#                 for index,entry in enumerate(header):
#                     data[entry.lower()] = row[index]
#                 # print(data)
#                 response = batch.put_item(
#                    Item=data
#                 )
#                 print(response)
