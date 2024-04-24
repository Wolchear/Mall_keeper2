import requests

service_url="http://plant_shop:5000"

def init_plants_list():
	response = requests.get(f'{service_url}/plants')
	if response.status_code == 200:
		return response.json()
	return None

def create_new_plant(name, plant_type, sellers):
	data = {"name": name,
		"type": plant_type,
		"sellers": sellers}
	headers = {"Content-Type": "application/json"}
	response = requests.post(f'{service_url}/plants', json=data, headers=headers)
	return response.status_code

