# pokemon_utilities.py

import boto3

class Utilities:
    def __init__(self, filename='PokemonDB.json'):
        self.dynamodb = boto3.resource('dynamodb')
        self.table = self.dynamodb.Table('Pokemon')
        
    def insert_pokemon(self, pokemon_name, weight, height):
        response = self.table.put_item(
            Item={
                'PokemonName': str(pokemon_name),
                'Weight': int(weight),
                'Height': int(height)
            }
        )
        if response['ResponseMetadata']['HTTPStatusCode'] == 200:
            print("Item added successfully!")
        else:
            print("Error adding item.")
    
    def display(self, name, height, weight):
        print(f"The pokemon is: {name}\nweights: {weight}\nheights is: {height}")
        if not name or not height or not weight:
            print("Error: Missing Pokémon details.")
    
    def is_in_data_base(self, pokemon_name):
        response = self.table.get_item(Key={'PokemonName': pokemon_name})
        if 'Item' in response:
            weight = response['Item']['Weight']
            height = response['Item']['Height']
            print(f"pokemon named: {pokemon_name} is already in the database")
            print(f"Height: {height}")
            print(f"Weight: {weight}")
            return True
        else:
            return False
