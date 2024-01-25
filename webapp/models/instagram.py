from instagrapi import Client
import json

config_data = open('config.json')
config = json.load(config_data)
config_data.close


username = config.get('ig_username')
password = config.get('ig_password')

cl = Client()
cl.login(username, password)

user_id = cl.user_id_from_username(username)
medias = cl.user_medias(user_id, 5)

print(user_id)
print(medias)