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
		return jsonify({'error': 'plant_name is Null'}), 400
				
	if plant_type is None:
		return jsonify({'error': 'plant_type is Null'}), 400
	
	if plant_type != 'flower' and plant_type != 'plant' and plant_type !='tree':
		return jsonify({'error': 'forbidden plant_type',
				'possible_types':'flower, plant, tree'}), 400
	
	return_code = pc.create_new_plant(plant_name, plant_type, sellers)
	
	if return_code == 201:
		plants_list = pc.init_plants_list()
		mall.available_plants = plants_list
		return jsonify({'plant_type': plant_type,
				'plant_name': plant_name}), 201



### Shops

@app.route('/shops', methods=['GET'])
def get_shops():
	shops = mall.getShopListByFloor()
	return jsonify(shops)

@app.route('/shops/<int:shop_id>', methods=['GET'])
def get_shop(shop_id):
	shop = mall.getShopById(shop_id)
	if shop is None:
		return jsonify({'error': 'Shop not found'}), 404
	return jsonify(shop.as_dict())


@app.route('/shops', methods=['POST'])
def add_shop():
	new_shop = request.json
	shop_name = new_shop.get('name')
	shop_floor = new_shop.get('floor')
	shop_type = new_shop.get('type')
	if shop_floor is None or shop_floor == "":
		return jsonify({'error':'shop_floor is Null'}), 400
		
	if shop_name is None or shop_name == "":
		return jsonify({'error':'shop_name is Null'}), 400
	
	if mall.if_shop_exists_by_name_floor(shop_name, shop_floor):
		return jsonify({'error':'Shop on this floor already exists'}), 400
	
	available_plants = pc.init_plants_list()
	if available_plants is None:
		return jsonify({'error':'Could not fetch any plants'}), 404
	
	mall.add_shop(shop_name, shop_floor)
	shop = mall.getShopByName(shop_name, shop_floor)
	for plant in available_plants:
		if plant.get('type') == shop_type:
			shop.addGood(plant.get('name'), plant.get('type'))
	
	return jsonify(shop.as_dict()), 201

@app.route('/shops/<int:shop_id>', methods=['PUT'])
def update_shop(shop_id):
	updated_data = request.json
	new_name = updated_data.get('new_name')
	new_floor = updated_data.get('new_floor')
	
	shop = mall.getShopById(shop_id)
	if shop is None:
		return jsonify({'error': 'Shop not found'}), 404
	
	if(mall.if_wrong_shop_update(new_name, new_floor)):
		return jsonify({'error': 'Shop on this floor already exists'}), 400
	
	shop.name = new_name
	shop.floor = int(new_floor)
	for worker in shop.workers:
		worker.shop = new_name
	
	return jsonify(shop.as_dict()), 200
	
@app.route('/shops/<int:shop_id>', methods=['DELETE'])
def delete_shop(shop_id):
	shop = mall.getShopById(shop_id)
	if shop is None:
		return jsonify({'error': 'Shop not found'}), 404

	mall.shops.remove(shop)
	return jsonify({'message': 'Shop deleted successfully'}), 200

### Good ####################################################################################################################################
@app.route('/shops/<int:shop_id>/goods', methods=['GET'])
def get_shop_goods(shop_id):
	shop = mall.getShopById(shop_id)
	if shop is None:
		return jsonify({'error': 'Shop not found'}), 404
		
	if not shop.goods:
		return jsonify({'error': 'Where is no goods in shop'}), 404
	
	return jsonify([good.as_dict() for good in shop.goods])
	
@app.route('/shops/<int:shop_id>/goods/<int:good_id>', methods=['GET'])
def get_good(shop_id,good_id):
	shop = mall.getShopById(shop_id)
	if shop is None:
		return jsonify({'error': 'Shop not found'}), 404
	good = shop.getGoodById(good_id)	
	if good is None:
		return jsonify({'error': 'Good not found'}), 404
	
	return jsonify([good.as_dict() for good in shop.goods])
	
@app.route('/shops/<int:shop_id>/goods', methods=['POST'])
def add_good(shop_id):
	new_good = request.json
	good_name = new_good.get('good_name')
	good_type = new_good.get('good_type')
	
	if good_name is None or good_name == "":
		return jsonify({'error':'good_name is Null'}), 400
		
	if good_type is None or good_type == "":
		return jsonify({'error':'good_type is Null'}), 400
	
	if shop_id is None or shop_id == "":
		return jsonify({'error':'shop_id is Null'}), 400
	
	shop = mall.getShopById(shop_id)
	if shop is None:
		return jsonify({'error': 'Shop not found'}), 404
		
	good = shop.getGood(good_name)
	if good:
		return jsonify({'error':' Good already exist'}), 400
		
	shop.addGood(good_name,good_type)
	good = shop.getGood(good_name)
	return jsonify(good.as_dict()), 201

@app.route('/shop/<int:shop_id>/goods/<int:good_id>', methods=['PUT'])
def update_good(shop_id, worker_id):
	updated_good = request.json
	good_name = updated_good.get('good_name')
	good_type = updated_good.get('good_type')
	
	shop = mall.getShopById(shop_id)
	if shop is None:
		return jsonify({'error': 'Shop not found'}), 404
		
	good = shop.getGood(good_name)
	if good:
		return jsonify({'error':' Good already exist'}), 400
	
	good.name = good_name
	good.good_type = good_type
	
	return jsonify(good.as_dict()), 200

@app.route('/shops/<int:shop_id>/goods/<int:good_id>', methods=['DELETE'])
def delete_good(shop_id, good_id):
	shop = mall.getShopById(shop_id)
	if shop is None:
		return jsonify({'error': 'Shop not found'}), 404
	
	if good_id is None:
		return jsonify({'error': 'Good_id is none'}), 400
	
	good_to_delete = None	
	for good in shop.goods:
		if good.good_id == good_id:
			good_to_delete = good
			break
	
	if good_to_delete is None:
		return jsonify({'error': 'Could not find good in shop'}), 404

	shop.goods.remove(good_to_delete)
	return jsonify({'message': 'Good deleted successfully'}), 200


#### Workers ##########################################################################################################
@app.route('/shops/<int:shop_id>/workers/<int:worker_id>', methods=['GET'])
def get_workers_by_mall_id(shop_id, worker_id):
	shop = mall.getShopById(shop_id)
	if shop is None:
		return jsonify({'error': 'Shop not found'}), 404
	
	worker = shop.getWorkerById(worker_id)
	if worker is None:
		return jsonify({'error': 'Worker not found'}), 404
	
	return jsonify(worker.as_dict())
    
@app.route('/workers', methods=['GET'])
def get_all_mall_workers():
	mall.update_workers_set()
	all_workers = mall.workers
	if all_workers is None:
		return jsonify({'error': 'No workers in a mall'}), 404
	return jsonify([worker.as_dict() for worker in all_workers])
    


@app.route('/shops/<int:shop_id>/workers', methods=['POST'])
def add_worker(shop_id):
	new_worker = request.json
	worker_name = new_worker.get('worker_name')
	worker_surname = new_worker.get('worker_surname')
	worker_sex = new_worker.get('sex')
	worker_position = new_worker.get('position')
	worker_salary = new_worker.get('salary')
	
	shop = mall.getShopById(shop_id)
	if shop is None:
		return jsonify({'error': 'Shop not found'}), 404
	
	if worker_name is None or worker_name == '':
		return jsonify({'error':'worker_name is Null'}), 400
	
	if worker_surname is None or worker_surname == '':
		return jsonify({'error':'worker_surname is Null'}), 400
	
	if worker_sex is None or worker_sex == '':
		return jsonify({'error':'worker_sex is Null'}), 400
		
	if worker_position is None or worker_position == '':
		return jsonify({'error':'worker_position is Null'}), 400
	
	if worker_salary is None or worker_salary == '':
		return jsonify({'error':'worker_salary is Null'}), 400
	
	worker = shop.getWorker(worker_name, worker_surname, worker_sex)
	if worker is not None:
		return jsonify({'error': 'Worker already exists'}), 404
	
	shop.addWorker(worker_name, worker_surname, worker_sex, worker_position, worker_salary)
	new_worker = shop.getWorker(worker_name, worker_surname, worker_sex)
	return jsonify(new_worker.as_dict()), 201



@app.route('/shops/<int:shop_id>/workers/<int:worker_id>', methods=['PUT'])
def update_worker(shop_id, worker_id):
	updated_worker = request.json
	new_name = updated_worker.get('worker_name')
	new_surname = updated_worker.get('worker_surname')
	new_sex = updated_worker.get('sex')
	new_salary = updated_worker.get('salary')
	new_position = updated_worker.get('position')
	
	shop = mall.getShopById(shop_id)
	if shop is None:
		return jsonify({'error': 'Shop not found'}), 404
	
	worker = shop.getWorkerById(worker_id)
	if worker is None:
		return jsonify({'error': 'Worker not found'}), 404
	
	if new_name is None or new_name == '':
		return jsonify({'error':'new_name is Null'}), 400
	
	if new_surname is None or new_surname == '':
		return jsonify({'error':'new_surname is Null'}), 400
	
	if new_sex is None or new_sex == '':
		return jsonify({'error':'new_sex is Null'}), 400
		
	if new_salary is None or new_salary == '':
		return jsonify({'error':'new_salary is Null'}), 400
	
	if new_position is None or new_position == '':
		return jsonify({'error':'new_position is Null'}), 400
	
	
	worker.salary = new_salary
	worker.position = new_position
	worker.name = new_name
	worker.surname = new_surname
	worker.sex = new_sex
	
	return jsonify(worker.as_dict()), 200


@app.route('/shops/<int:shop_id>/workers/<int:worker_id>', methods=['DELETE'])
def delete_worker(shop_id, worker_id):
	shop = mall.getShopById(shop_id)
	if shop is None:
		return jsonify({'error': 'Shop not found'}), 404
	
	worker = shop.getWorkerById(worker_id)
	if worker is None:
		return jsonify({'error': 'Worker not found'}), 404
		

	shop.workers.remove(worker)
	return jsonify({'message': 'Worker deleted successfully'}), 200


@app.route('/')
def index():
	return 'Move to'

if __name__ == '__main__':
	app.run(host='0.0.0.0', port=80, debug = True)
