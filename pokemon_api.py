# pokemon_api.s

import requests
import random

class GetApi:
    def pokemon_list(self):
        response = requests.get('https://pokeapi.co/api/v2/pokemon?limit=50')
        if response.status_code == 200:
            data = response.json()
            pokemon_dict = {i + 1: pokemon['name'] for i, pokemon in enumerate(data['results'])}
            return pokemon_dict
        else:
            print("Failed to retrieve data")
            return None

    def Get_random_pokemon(self, pokemon_dict):
        random_pokemon = random.choice(list(pokemon_dict.values()))
        return random_pokemon

    def get_pokemon_details(self, random_pokemon):
        try:
            response = requests.get(f'https://pokeapi.co/api/v2/pokemon/{random_pokemon}/')
            if response.status_code == 200:
                pokemon_details = response.json()
                Name = pokemon_details['name']
                Height = pokemon_details['height']
                Weight = pokemon_details['weight']
                return Name, Height, Weight
            else:
                print("Failed to retrieve data")
                return None, None, None
        except requests.exceptions.RequestException as err:
            print(f"Error occurred: {err}")
            return None, None, None
