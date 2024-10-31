import requests
import random
import json
import os
import boto3
from pokemon_api import GetApi  # Import the GetApi class from pokemon_api.py

            

class Utilities():
    
    #ets up an instance of the class with a filename (defaulting to 'PokemonDB.json') and an empty dictionary for storing Pokémon details
    def __init__(self, filename='PokemonDB.json'):
        self.dynamodb = boto3.resource('dynamodb') #This line initializes a DynamoDB resource using Boto3.
        self.table = self.dynamodb.Table('Pokemon') #This line retrieves a specific DynamoDB table named Pokemon
     
     
           
    #Function that responsible of inserting the pokemon details into dynamodb database
    def insert_pokemon(self,pokemon_name, weight, height):
    	
    	# Insert a new item
    	response = self.table.put_item( # used to create a new item in the table or replace an existing item
	    Item={
	    	'PokemonName': str(pokemon_name),  # Primary key
	    	'Weight': int(weight) , #inserting the value of weight into created attribute called "Weight"
	    	'Height': int(height)   #inserting the value of height into created attribute called "Height"
	     }
    	)
    	
    	if response['ResponseMetadata']['HTTPStatusCode'] == 200: #A status code of 200 indicates that the operation was successful.
    		print("Item added successfully!")
    	else:
    		print("Error adding item.")
	    
    # Function that responsible of displaying results of pokemon information 
    def display(self,name, height, weight):#gets the pokemons info 
        self.name = name #store the pokemons name at self.name
        self.height = height #store the pokemons height at self.height
        self.weight = weight #store the pokemons weight at self.weight
        
        #variable that stores all the pokemon info with string
        self.poke_info=print(f"The pokemon is: {self.name}\nweights: {self.weight} \nheights is: {self.height}")
        
        if self.name is None: #if self.poke_info has no value print error
            #print("No Pokémon details available.")
            return print("No Pokémon name available.")
        
        if self.height is None: #if self.poke_info has no value print error
            #print("No Pokémon details available.")
            return print("No Pokémon height available.")
    
        if self.weight is None: #if self.poke_info has no value print error
            
            #print("No Pokémon details available.")
            return print("No Pokémon weight available.")
    
    ##function that responsible of checking if the random pokemon information already in dynamodb Database 
    def is_in_data_base(self,pokemon_name):
    
    	# Retrieve the item by Pokémon name
    	response = self.table.get_item(Key={'PokemonName': pokemon_name})

    	# Check if the item exists
    	if 'Item' in response: #This line checks if the key 'Item' is present in the response dictionary (if pokemon_name is in database as a key that have details).
    		weight = response['Item']['Weight']
    		height = response['Item']['Height']
    		print(f"pokemon named: {pokemon_name} is already in the database")
    		print(f"Height: {height}")  # You can specify the unit if known
    		print(f"Weight: {weight}")
	    	return True #Pokémon exists
		
    	else:
	    	return False #Pokémon does not exist
         



###main##
        
#define class variables
get_api = GetApi()
utilities = Utilities()

#create break flag
flag = 0
#get pokemons name list by api and store in pokemon_list
pokemon_list = get_api.pokemon_list()#get pokemon list

print("----Welcome to the pokemon generator!-----")
while flag==0:
    print("\n")
    print("-----------------------------------")
    ans = input("Do you want to generate new pokemon? (y/n): ")
    if ans == 'y':
        
        random_pokemon = get_api.Get_random_pokemon(pokemon_list) #get random pokemon from the pokemon list
        in_data_base = utilities.is_in_data_base(random_pokemon) #check if the random pokemon already in database it True it will print the details with relevant message
        
        if in_data_base == False:#if random poke not already in database do the next steps 
            Name,Height,Weight = get_api.get_pokemon_details(random_pokemon)#get pokemon details info
            
            utilities.display(Name,Height,Weight)#display pokemon details info
            utilities.insert_pokemon(Name,Height,Weight)#store the pokemon detailes in dynamodb database'
            
            
    elif ans == 'n':
        print("See you next time :)")
        flag = 1







    
    
    
    
    
