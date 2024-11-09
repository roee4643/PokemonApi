import boto3
from botocore.exceptions import ClientError

def create_table():
    dynamodb = boto3.resource('dynamodb')

    # Define KeySchema and AttributeDefinitions properly
    try: 
        table = dynamodb.create_table(
            TableName='Pokemon',
            KeySchema=[
                {
                    'AttributeName': 'PokemonName',  # Partition key
                    'KeyType': 'HASH'  # HASH = Partition key
                }
            ],
            AttributeDefinitions=[
                {
                    'AttributeName': 'PokemonName',
                    'AttributeType': 'S'  # String type for partition key
                }
                # You can add Weight if needed as a non-key attribute later
            ],
            ProvisionedThroughput={
                'ReadCapacityUnits': 10,
                'WriteCapacityUnits': 10  # Specify a value here
            }
        )
     # Wait until the table exist
        table.meta.client.get_waiter('table_exists').wait(TableName='Pokemon')
        print("Table created:", table)

    except ClientError as e:
        if e.response['Error']['Code'] == 'ResourceInUseException':
            print( "Table Pokemon is already exists.")
        else:
            print(f"Unexpected error: {e}")


# Call the function
create_table()
