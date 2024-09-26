import requests
import random
import json


class Pokemons():
    
    def get_pokemon_details(self,random_pokemon):
        self.random_pokemon = random_pokemon
        try:  
            response = requests.get(f'https://pokeapi.co/api/v2/pokemon/{self.random_pokemon}/')
            
            # Check if the request was successful
            if response.status_code == 200:
                self.pokemon_details = response.json() #store the response from API to self.pokemon_details
                
                #create variable that will present the relevant values from the details list and will be well presented
                poke_info = (
                    f"Name: {self.pokemon_details['name']}\n"
                    f"Height: {self.pokemon_details['height']}\n"
                    f"Weight: {self.pokemon_details['weight']}"
                )
                 
                return poke_info
            
            else:# if the request was unsuccessful print error
                return print("Failed to retrieve data")
            
        except requests.exceptions.HTTPError as http_err:
            print(f"HTTP error occurred: {http_err}")
        except requests.exceptions.RequestException as err:
            print(f"Error occurred: {err}")
  


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
        
        
    def is_in_DB(self):
        pass
    

class Utilities():
    
    def input(self):
        pass
    
    # function that responsible of displaying results of pokemon information 
    def display(self,poke_info):#gets the pokemons info 
        self.poke_info = poke_info #store the pokemons info at self.poke_info
        
        if self.poke_info is None: #if self.poke_info has no value print error
            print("No Pokémon details available.")
            return
        
        print(f"{self.poke_info}")
        
        
    # function that responsible of converrt the results of pokemon information to json format    
    def convert_to_json(self,data_to_convert):
         
        self.data_to_convert = data_to_convert
        # Parse the string
        json_data = {}
        for line in self.data_to_convert.split('\n'): #This line is iterating over each line in the string self.data_to_convert
            key, value = line.split(': ', 1)  # This line splits each line into two parts: key and value. The split(': ', 1) method divides the line at the first occurrence of the string ": ".
            json_data[key] = value  #This line adds the key and value pair to the json_data dictionary

        # Convert to JSON format
        #poke_info_json_display = json.dumps(json_data, indent=4) 
        
        return json_data #return the json_data of the pokemon info (returns the pokemon info in json format)
         
    # function that responsible of storing the json format of pokemon information in a json file named 'PokemonDB.json' that will use as our Data base   
    def store_in_PokemonDB_js(self,data_to_store):
        self.data_to_store = data_to_store #store the data to store(pokemon information in a json file) in self.data_to_store
        
        json_data = json.dumps(poke_info, indent=4)#json.dumps = This function is part of the json module in Python. It converts a Python object (like a dictionary) into a JSON-formatted string.
        filename = 'PokemonDB.json' #define file name
        # Write data to a JSON file
        with open(filename, 'w') as json_file:
            json.dump(self.data_to_store, json_file, indent=4)

        print(f"Data successfully written to {filename}")#print that data is stored

        


###main testing##
        
#define class variables
pokemon = Pokemons()
get_api = GetApi()
utilities = Utilities()


#get pokemon list
pokemon_list = get_api.pokemon_list()

#get random pokemon 
random_pokemon = get_api.Get_random_pokemon(pokemon_list)

#get pokemon details info
poke_info = pokemon.get_pokemon_details(random_pokemon)

#display pokemon details info
utilities.display(poke_info)

#get json data format pokemon info
json_data = utilities.convert_to_json(poke_info)

#store json pokemon info details in file name 'PokemonDB.json'
utilities.store_in_PokemonDB_js(json_data)






    
    
    
    
    