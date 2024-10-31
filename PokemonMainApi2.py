import requests
import random
import json
import os
import boto3
from pokemon_api import GetApi  # Import the GetApi class from pokemon_api.py
from pokemon_utilities import Utilities  # Import the Utilities class
            



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







    
    
    
    
    
