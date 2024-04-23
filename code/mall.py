import shop as shop
import good as good
import worker as worker
class Mall:
	def __init__(self):
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
		
		shop1_1.addWorker("Davina", "Keith")
		shop1_2.addWorker("Brynlee", "Larsen")
		shop1_1.addWorker("Kyleigh", "Porter")
		shop2_2.addWorker("Nancy", "Porter")
		shop2_1.addWorker("Richard", "Hebert")
		
		self.shops.extend([shop1_1, shop1_2, shop2_1, shop2_2, shop3_1])
		
		for shopa in self.shops:
			self.workers.extend(shopa.workers)
	
	def add_shop(self, name, floor):
		new_shop = shop.Shop(name, floor)
		self.shops.append(new_shop)
	
	def add_good(self, shop_id, good, good_type):
		for shop in self.shops:
			if shop.shop_id == shop_id:
				shop.addGood(good, good_type)
	
	def if_good_exists(self, shop_id, good_name):
		for shop in self.shops:
			if shop.shop_id == shop_id:
				for good in shop.goods:
					if(good_name == good.name):
						return True
		return False
			
	def add_worker(self, shop_id, name, surname):
		for shop in self.shops:
			if shop.shop_id == shop_id:
				shop.addWorker(name, surname)
	
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
		
	def if_shop_exists(self, shop_name, shop_floor):
		for shop in self.shops:
			if shop.name == shop_name and shop.floor == shop_floor:
				return True
		return False
	
	def if_shop_exists_by_id(self, shop_id):
		for shop in self.shops:
			if shop.shop_id == shop_id:
				return True
		return False
	
	def update_ids_after_shop_delete(self, shop_id):
		for shop in self.shops:
			if shop.shop_id > shop_id:
				shop.shop_id -=1
	
	def getShopListByFloor(self,):
		return [shop.as_dict() for shop in self.shops]
		
	def get_workers_by_mall_id(self, mall_id):
		for worker in self.workers:
			if worker.mall_id == mall_id:
				return worker
		return None
		
		
		
		
