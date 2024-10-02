import requests
import random
import json
import os


class Pokemons():
    pass
    
    
  


class GetApi():
    
    
    #function that responsible of get pokemon name list
    def pokemon_list(self):
        # Fetching  all pokemons data from the Pokémon API
        response = requests.get('https://pokeapi.co/api/v2/pokemon?limit=-1')
        if response.status_code == 200:# Check if the request was successful
            data = response.json() #store the information of pokemons into data
            pokemon_dict = {i + 1: pokemon['name'] for i, pokemon in enumerate(data['results'])} #use for loop to store all pokemons names into a list
            return pokemon_dict #return pokemons name list
        
        else:
            return print("Failed to retrieve data")
        

    #function that responsible of geting random pokemon name from the list
    def Get_random_pokemon(self,pokemon_dict):
        self.pokemon_dict=pokemon_dict
        random_pokemon = random.choice(list(pokemon_dict.values())) #pick random choice from the pokemon name list
        return random_pokemon #return the random pokemon name
    
    def get_pokemon_details(self,random_pokemon):
        self.random_pokemon = random_pokemon
        try:  
            response = requests.get(f'https://pokeapi.co/api/v2/pokemon/{self.random_pokemon}/')
            
            # Check if the request was successful
            if response.status_code == 200:
                self.pokemon_details = response.json() #store the response from API to self.pokemon_details
                
                #create variable that will present the relevant values from the details list and will be well presented
                Name =self.pokemon_details['name']
                Height=self.pokemon_details['height']
                Weight= self.pokemon_details['weight']
                
                 
                return Name,Height,Weight
            
            else:# if the request was unsuccessful print error
                return print("Failed to retrieve data")
            
        except requests.exceptions.HTTPError as http_err:
            print(f"HTTP error occurred: {http_err}")
        except requests.exceptions.RequestException as err:
            print(f"Error occurred: {err}")
        
        
    

class Utilities():
    
    #ets up an instance of the class with a filename (defaulting to 'PokemonDB.json') and an empty dictionary for storing Pokémon details
    def __init__(self, filename='PokemonDB.json'):
        self.filename = filename
        self.pokemon_details = {}
        
    #attempts to load JSON data from a specified file. If the file exists, it reads and parses the data into a Python object; if it does not exist, it simply returns an empty dictionary.    
    def load_data(self):
        if os.path.exists(self.filename):
            with open(self.filename, 'r') as file:
                return json.load(file)
        return {}
    
    #takes a data object, opens a specified JSON file for writing, and saves the data in JSON format.
    def save_data(self, data):
        with open(self.filename, 'w') as file:
            json.dump(data, file, indent=4)
            
            
    #Loads existing Pokémon data from a JSON file.
    #Updates the data with new or modified height and weight for a specified Pokémon (identified by name).
    #Saves the updated data back to the JSON file       
    def add_pokemon(self, name, height, weight):
        
        #these lines are storing specific attributes (name, height, and weight) of a Pokémon into the self.pokemon_details dictionary.
        self.pokemon_details['name'] = name
        self.pokemon_details['height'] = height
        self.pokemon_details['weight'] = weight
        # Load existing data
        existing_data = self.load_data()
        
        #This line adds or updates an entry in the existing_data dictionary using the variable name as the key.
        existing_data[name] = { 
                'height': height,
                'weight': weight
            }
        
        # Save updated data back to the JSON file
        try:
            self.save_data(existing_data)
            print(f"{name} added to the database.")
            
        except Exception as e:
            print(f"Failed to save data: {e}")
        
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
    
    ##function that responsible of checking if the random pokemon information already in Database 'PokemonDB.json'
    def is_in_data_base(self,name):
        self.pokemon_details['name'] = name
        existing_data = self.load_data()
         # Check if the Pokémon name already exists
        if name not in existing_data:
            # Save updated data back to the JSON file
            return False
        
        else:
            print(f"{name} already exists in the database.")
            print(existing_data[name])
            return True
         



###main testing##
        
#define class variables
#pokemon = Pokemons()
get_api = GetApi()
utilities = Utilities()

#create break flag
flag = 0
#get pokemons name list by api and store in pokemon_list
pokemon_list = get_api.pokemon_list()#get pokemon list

print("Welcome to the pokemon generator!")
while flag==0:
    ans = input("do you want to generate new pokemon? (y/n): ")
    if ans == 'y':
        
        random_pokemon = get_api.Get_random_pokemon(pokemon_list) #get random pokemon from the pokemon list
        in_data_base = utilities.is_in_data_base(random_pokemon) #check if the random pokemon already in database it True it will print the details with relevant message
        
        if in_data_base == False:#if random poke not already in database do the next steps 
            Name,Height,Weight = GetApi.get_pokemon_details(random_pokemon)#get pokemon details info
            utilities.add_pokemon(Name,Height,Weight)#store json pokemon info details in file name 'PokemonDB.json'
            utilities.display(Name,Height,Weight)#display pokemon details info
            
    elif ans == 'n':
        print("See you next time :)")
        flag = 1







    
    
    
    
    