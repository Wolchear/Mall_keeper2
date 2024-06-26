import shop as shop
import good as good
import worker as worker
class Mall:
	def __init__(self):
		self.available_plants = []
		self.shops=[]
		self.workers=[]
		shop1_1 = shop.Shop("Maxima", 1)
		shop1_2 = shop.Shop("Technorama", 1)
		shop2_1 = shop.Shop("Clothes shop", 2)
		shop2_2 = shop.Shop("FLOWER STORE", 2)
		shop3_1 = shop.Shop("test_store", 3)
		
		shop1_1.addGood("Milk", "diary product")
		shop1_2.addGood("Iphone", "smartphone")
		shop1_1.addGood("Chocolate", "Sweets")
		shop2_1.addGood("Jeans", "clothes")
		shop2_2.addGood("Rose", "flower")
		shop2_2.addGood("Tulip", "flower")
		
		shop1_1.addWorker("Davina", "Keith", 'Female',  1000, 'Manager')
		shop1_2.addWorker("Brynlee", "Larsen", 'Female', 760, 'Seller')
		shop1_1.addWorker("Kyleigh", "Porter", 'Female',  800, 'Seller')
		shop2_2.addWorker("Nancy", "Porter", 'Female', 1100,  'Florist')
		shop2_1.addWorker("Richard", "Hebert", 'Male', 780, 'Seller')
		
		self.shops.extend([shop1_1, shop1_2, shop2_1, shop2_2, shop3_1])
		
		for shopa in self.shops:
			self.workers.extend(shopa.workers)
			
	
	def if_worker_exists(self, worker_id):
		for worker in self.workers:
			if worker.mall_id == worker_id:
				return True;
		return False;
	
	def checkAvailablePlants(self, plant_name):
		for plant in self.available_plants:
			if 'name' in plant and plant['name'] == plant_name:
				return True
		return False
	
	def getShopByName(self, name, floor):
		for shop in self.shops:
			if shop.name == name and shop.floor == floor:
				return shop
		return None
	
	def getShopById(self, shop_id):
		for shop in self.shops:
			if shop.shop_id == shop_id:
				return shop
		return None	
	
	
	def add_shop(self, name, floor):
		new_shop = shop.Shop(name, floor)
		self.shops.append(new_shop)
	
	def add_good(self, shop_id, good, good_type):
		for shop in self.shops:
			if shop.shop_id == shop_id:
				shop.addGood(good, good_type)
	
	def getShopWorker(self,shop_id, worker_name, worker_surname):
		for shop in self.shops:
			if shop.shop_id == shop_id:
				for worker in shop.workers:
					if worker.name == worker_name and worker.surname == worker_surname:
						return worker
		return None
	
	
	def if_good_exists(self, shop_id, good_name):
		for shop in self.shops:
			if shop.shop_id == shop_id:
				for good in shop.goods:
					if(good_name == good.name):
						return True
		return False
			
	def add_worker(self, shop_id, name, surname, sex,salary, position):
		for shop in self.shops:
			if shop.shop_id == shop_id:
				shop.addWorker(name, surname, sex,salary, position)
	
	def get_shop_goods(self, shop_id):
		for shop in self.shops:
			if shop.shop_id == shop_id:
				return shop.goods
		return None
	
	def update_workers_set(self):
		self.workers=[]
		for shop in self.shops:
			self.workers.extend(shop.workers)
	
	def if_wrong_shop_update(self, shop_name, shop_floor):
		for shop in self.shops:
			if shop.name == shop_name and shop.floor == shop_floor:
				return True
		return False
		
	
	def if_shop_exists_by_id(self, shop_id):
		for shop in self.shops:
			if shop.shop_id == shop_id:
				return True
		return False
	
	def if_shop_exists_by_name_floor(self, name, floor):
		for shop in self.shops:
			if shop.name == name and shop.floor == floor:
				return True
		return False
	
	def getShopListByFloor(self,):
		return [shop.as_dict() for shop in self.shops]	
