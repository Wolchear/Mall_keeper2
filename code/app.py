from flask import Flask, request, jsonify
from mall import Mall
app = Flask(__name__)

mall = Mall()

@app.route('/shops', methods=['GET'])
def get_shops():
	shops = mall.getShopListByFloor()
	return jsonify(shops)

@app.route('/workers', methods=['GET'])
def get_workers_by_mall_id():
	mall_id = request.args.get('mall_id')
	workers = mall.get_workers_by_mall_id(int(mall_id))
	if workers is None:
		return jsonify({'error': 'Woker not found',
				"http_status": 404,
				'worker_id': int(mall_id)}), 404
	return jsonify(workers)
    
@app.route('/workers', methods=['GET'])
def get_all_mall_workers():
	mall.update_workers_set()
	all_workers = mall.workers
	return jsonify([worker.as_dict() for worker in all_workers])
    
@app.route('/shops/goods', methods=['GET'])
def get_shop_goods():
	shop_id = request.args.get('shop_id')
	goods = mall.get_shop_goods(int(shop_id))
	
	if not mall.if_shop_exists_by_id(int(shop_id)):
		return jsonify({'error': 'Shop not found',
				"http_status": 404,
				'shop_id': int(shop_id)}), 404
	if not goods:
		return jsonify({'error': 'Where is no goods in shop',
				"http_status": 404,
				'shop_id': int(shop_id)}), 404
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

@app.route('/shops/goods', methods=['POST'])
def add_good():
	new_good = request.json
	good_name = new_good.get('good_name')
	good_type = new_good.get('good_type')
	shop_id = new_good.get('shop_id')
	
	if good_name is None or good_name == "":
		return jsonify({'error':'good_name is Null',
				"http_status": 400}), 400
		
	if good_type is None or good_type == "":
		return jsonify({'error':'good_type is Null',
				"http_status": 400}), 400
	
	if shop_id is None or shop_id == "":
		return jsonify({'error':'shop_id is Null',
				"http_status": 400}), 400
	
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

@app.route('/workers', methods=['POST'])
def add_worker():
	new_worker = request.json
	worker_name = new_worker.get('worker_name')
	worker_surname = new_worker.get('worker_surname')
	shop_id = new_worker.get('shop_id')
	
	if not mall.if_shop_exists_by_id(shop_id):
		return jsonify({'error': 'Shop not found',
				"http_status": 404,
				'shop_id': shop_id}), 404
	
	if worker_name is None or worker_name is '':
		return jsonify({'error':'worker_name is Null',
				"http_status": 400}), 400
	
	if worker_surname is None or worker_surname == '':
		return jsonify({'error':'worker_surname is Null',
				"http_status": 400}), 400
		
	mall.add_worker(shop_id, worker_name, worker_surname)
	
	return jsonify({'message':'New worker sucesffuly added',
			"http_status": 201,
			'shop_id': shop_id,
			'worker_name': worker_name,
			'worker_surname': worker_surname}), 201

@app.route('/shops', methods=['PUT'])
def update_shop():
	updated_data = request.json
	shop_id = updated_data.get('shop_id')
	new_name = updated_data.get('new_name')
	new_floor = updated_data.get('new_floor')
	
	if(mall.if_shop_exists(new_name, new_floor)):
		return jsonify({'error': 'Shop not found',
				"http_status": 404,
				'shop_name': new_name,
				'shop_floor': new_floor}), 404
	
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

@app.route('/shops', methods=['DELETE'])
def delete_shop():
	shop_to_delete = None
	delete_data = request.json
	shop_id = delete_data.get('shop_id')
	
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

@app.route('/shops/goods', methods=['DELETE'])
def delete_good():
	shop_to_update = None
	delete_data = request.json
	shop_id = delete_data.get('shop_id')
	good_name = delete_data.get('good_name')
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
		if good.name == good_name:
			good_to_delete = good
			break
	
	if good_to_delete is None:
		return jsonify({'error': 'Could not find good in shop',
				"http_status": 404,
				'shop_id': shop_id,
				'good_name': good_name}), 404

	shop_to_update.goods.remove(good_to_delete)
	return jsonify({'message': 'Good deleted successfully',
			"http_status": 200,
			'shop_id': shop_id,
			'good_name': good_name}), 200

@app.route('/')
def index():
	return 'Move to'

if __name__ == '__main__':
	app.run(host='0.0.0.0', port=5000, debug = True)
