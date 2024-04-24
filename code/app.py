from flask import Flask, request, jsonify
from mall import Mall
import plants_connection as pc
app = Flask(__name__)

mall = Mall()
plants_list = pc.init_plants_list()
mall.available_plants = plants_list


@app.route('/plants', methods=['POST'])
def add_plant():
	new_plant = request.json
	plant_name = new_plant.get('name')
	plant_type = new_plant.get('type').lower()
	sellers=[]
	print (plant_type)
	if plant_name is None:
		return jsonify({'error': 'plant_name is Null',
				"http_status": 400,}), 400
				
	if plant_type is None:
		return jsonify({'error': 'plant_type is Null',
				"http_status": 400,}), 400
	
	if plant_type != 'flower' and plant_type != 'plant' and plant_type !='tree':
		return jsonify({'error': 'forbidden plant_type',
				'possible_types':'flower, plant, tree',
				'plant_type': plant_type,
				"http_status": 400,}), 400
	
	return_code = pc.create_new_plant(plant_name, plant_type, sellers)
	
	if return_code == 201:
		plants_list = pc.init_plants_list()
		mall.available_plants = plants_list
		return jsonify({'message': 'Plant sucsessfuly added',
				'plant_type': plant_type,
				'plant_name': plant_name,
				"http_status": 201}), 201
	return jsonify({'error': 'error'}), 400


@app.route('/shops', methods=['GET'])
def get_shops():
	shops = mall.getShopListByFloor()
	return jsonify(shops)

@app.route('/workers/<int:mall_id>', methods=['GET'])
def get_workers_by_mall_id(mall_id):
	workers = mall.get_workers_by_mall_id(mall_id)
	if workers is None:
		return jsonify({'error': 'Woker not found',
				"http_status": 404,
				'worker_id': mall_id}), 404
	return jsonify(workers.as_dict())
    
@app.route('/workers', methods=['GET'])
def get_all_mall_workers():
	mall.update_workers_set()
	all_workers = mall.workers
	return jsonify([worker.as_dict() for worker in all_workers])
    
@app.route('/shops/<int:shop_id>/goods', methods=['GET'])
def get_shop_goods(shop_id):
	goods = mall.get_shop_goods(shop_id)
	
	if not mall.if_shop_exists_by_id(shop_id):
		return jsonify({'error': 'Shop not found',
				"http_status": 404,
				'shop_id': shop_id}), 404
	if not goods:
		return jsonify({'error': 'Where is no goods in shop',
				"http_status": 404,
				'shop_id': shop_id}), 404
	return jsonify([good.as_dict() for good in goods])

@app.route('/shops', methods=['POST'])
def add_shop():
	new_shop = request.json
	shop_name = new_shop.get('name')
	shop_floor = new_shop.get('floor')
	
	if shop_floor is None or shop_name is None:
		return jsonify({'error':' No floor or name',
				"http_status": 400}), 400
		
	mall.add_shop(shop_name, shop_floor)

	message = 'New shop successfully added'
	return jsonify({'message':message,
			'shop_name': shop_name,
			'shop_floor':shop_floor,
			"http_status": 201 }), 201

@app.route('/shops/<int:shop_id>/goods', methods=['POST'])
def add_good(shop_id):
	new_good = request.json
	good_name = new_good.get('good_name')
	good_type = new_good.get('good_type')
	
	if good_name is None or good_name == "":
		return jsonify({'error':'good_name is Null',
				"http_status": 400}), 400
		
	if good_type is None or good_type == "":
		return jsonify({'error':'good_type is Null',
				"http_status": 400}), 400
	
	if shop_id is None or shop_id == "":
		return jsonify({'error':'shop_id is Null',
				"http_status": 400}), 400
	
	if good_type.lower() == "plant":
		if not mall.checkAvailablePlants(good_name):
			return jsonify({'error':'This plant is not available now',
					'good_name':good_name,
					'good_type':good_type,
					"http_status": 404}), 404
					
	if good_type.lower() == "flower":
		if not mall.checkAvailablePlants(good_name):
			return jsonify({'error':'This flower is not available now',
					'good_name':good_name,
					'good_type':good_type,
					"http_status": 404}), 404
	
	if good_type.lower() == "tree":
		if not mall.checkAvailablePlants(good_name):
			return jsonify({'error':'This tree is not available now',
					'good_name':good_name,
					'good_type':good_type,
					"http_status": 404}), 404
	
	if(mall.if_good_exists(shop_id, good_name)):
		return jsonify({'error':' Good already exist',
				"http_status": 400}), 400
	mall.add_good(shop_id, good_name,good_type)
	message = 'New good sucesffuly added'
	return jsonify({'message':message,
			"http_status": 201,
			'shop_id': shop_id,
			'good_name':good_name,
			'good_type':good_type}), 201

@app.route('/shops/<int:shop_id>/workers', methods=['POST'])
def add_worker(shop_id):
	new_worker = request.json
	worker_name = new_worker.get('worker_name')
	worker_surname = new_worker.get('worker_surname')
	worker_sex = new_worker.get('sex')
	worker_position = new_worker.get('position')
	worker_salary = new_worker.get('salary')
	
	if not mall.if_shop_exists_by_id(shop_id):
		return jsonify({'error': 'Shop not found',
				"http_status": 404,
				'shop_id': shop_id}), 404
	
	if worker_name is None or worker_name == '':
		return jsonify({'error':'worker_name is Null',
				"http_status": 400}), 400
	
	if worker_surname is None or worker_surname == '':
		return jsonify({'error':'worker_surname is Null',
				"http_status": 400}), 400
		
	mall.add_worker(shop_id, worker_name, worker_surname, worker_sex, worker_salary, worker_position)
	
	return jsonify({'message':'New worker sucesffuly added',
			"http_status": 201,
			'shop_id': shop_id,
			'worker_name': worker_name,
			'worker_surname': worker_surname,
			'worker_sex': worker_sex,
			'worker_salary': worker_salary,
			'worker_position': worker_position}), 201

@app.route('/shops/<int:shop_id>', methods=['PUT'])
def update_shop(shop_id):
	updated_data = request.json
	new_name = updated_data.get('new_name')
	new_floor = updated_data.get('new_floor')
	
	if not mall.if_shop_exists_by_id(shop_id):
		return jsonify({'error': 'Shop not found',
				"http_status": 404,
				'shop_id': shop_id}), 404
	
	if(mall.if_wrong_shop_update(new_name, new_floor)):
		return jsonify({'error': 'Shop on this floor already exists',
				"http_status": 400,
				'shop_name': new_name,
				'shop_floor': new_floor}), 400
	
	for shop in mall.shops:
		if shop.shop_id == shop_id:
			old_name = shop.name
			old_floor = shop.floor
			shop.name = new_name
			shop.floor = new_floor
			break
	
	return jsonify({'message': 'Shop updated successfully',
			"http_status": 200,
			'old_name':old_name,
			'old_floor': old_floor,
			'new_name': new_name,
			'new_floor': new_floor}), 200

@app.route('/workers/<int:mall_id>', methods=['PUT'])
def update_worker(mall_id):
	updated_worker = request.json
	new_salary = updated_worker.get('salary')
	new_position = updated_worker.get('position')
	
	if not mall.if_worker_exists( mall_id):
		return jsonify({'error': 'Worker not found',
				"http_status": 404,
				'worker_mall_id': mall_id}), 404
	
	for worker in mall.workers:
		if worker.mall_id == mall_id:
			old_salary = worker.salary
			old_position = worker.position
			worker.salary = new_salary
			worker.position = new_position
			break
	
	return jsonify({'message': 'Worker updated successfully',
			"http_status": 200,
			'mall_id':mall_id,
			'old_salary':old_salary,
			'old_position': old_position,
			'new_salary': new_salary,
			'new_position': new_position}), 200





@app.route('/shops/<int:shop_id>', methods=['DELETE'])
def delete_shop(shop_id):
	shop_to_delete = None
	if not mall.if_shop_exists_by_id(shop_id):
		return jsonify({'error': 'Shop not found',
				"http_status": 404,
				'shop_id': shop_id}), 404

	for shop in mall.shops:
		if shop.shop_id == shop_id:
			shop_to_delete = shop
			break
	
	mall.shops.remove(shop_to_delete)
	mall.update_ids_after_shop_delete(shop_id)
	return jsonify({'message': 'Shop deleted successfully',
			"http_status": 200,
			"shop_name": shop_to_delete.name,
			"shop_id": shop_id,
			"shop_floor": shop_to_delete.floor}), 200

@app.route('/shops/<int:shop_id>/goods/<int:good_id>', methods=['DELETE'])
def delete_good(shop_id, good_id):
	shop_to_update = None
	for shop in mall.shops:
		if shop.shop_id == shop_id:
			shop_to_update = shop
			break

	if not mall.if_shop_exists_by_id(shop_id):
		return jsonify({'error': 'Shop not found',
				"http_status": 404,
				'shop_id': shop_id}), 404
		
	good_to_delete = None
	for good in shop_to_update.goods:
		if good.good_id == good_id:
			good_to_delete = good
			good_name = good.name
			good_type = good.good_type
			break
	
	if good_to_delete is None:
		return jsonify({'error': 'Could not find good in shop',
				"http_status": 404,
				'shop_id': shop_id,
				'good_id': good_id}), 404

	shop_to_update.goods.remove(good_to_delete)
	return jsonify({'message': 'Good deleted successfully',
			"http_status": 200,
			'shop_id': shop_id,
			'good_id': good_id,
			'good_type': good_type,
			'good_name': good_name}), 200

@app.route('/shops/<int:shop_id>/workers/<int:worker_id>', methods=['DELETE'])
def delete_worker(shop_id, worker_id):
	shop_to_update = None
	for shop in mall.shops:
		if shop.shop_id == shop_id:
			shop_to_update = shop
			break

	if not mall.if_shop_exists_by_id(shop_id):
		return jsonify({'error': 'Shop not found',
				"http_status": 404,
				'shop_id': shop_id}), 404
		
	worker_to_delete = None
	for worker in shop_to_update.workers:
		if worker.id_in_shop == worker_id:
			worker_to_delete = worker
			worker_name = worker.name
			worker_surname = worker.surname
			worker_salary = worker.salary
			worker_position = worker.position
			break
	
	if worker_to_delete is None:
		return jsonify({'error': 'Could not find good in shop',
				"http_status": 404,
				'shop_id': shop_id,
				'good_id': good_id}), 404

	shop_to_update.workers.remove(worker_to_delete)
	return jsonify({'message': 'Worker deleted successfully',
			"http_status": 200,
			'worker_name': worker_name,
			'worker_surname': worker_surname,
			'worker_salary': worker_salary,
			'worker_position': worker_position}), 200


@app.route('/')
def index():
	return 'Move to'

if __name__ == '__main__':
	app.run(host='0.0.0.0', port=80, debug = True)
