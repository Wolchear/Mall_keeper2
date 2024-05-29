import good as good
import worker as worker
class Shop:
	shop_id =1;
	def __init__(self, name, floor):
		self.shop_id = Shop.shop_id
		Shop.shop_id +=1
		self.name = name
		self.floor = floor
		self.goods = []
		self.workers = []
		self.worker_id=1
		self.good_id =1
		self.shop_type = "Unspecified"
		
	def addGood(self, good_name, good_type):
		self.goods.append(good.Good(good_name, good_type, self.good_id))
		self.good_id +=1
		
	def addWorker(self, name, surname, sex, position, salary):
		self.workers.append(worker.Worker(name, surname, self.name, self.worker_id, sex, position, salary))
		self.worker_id += 1
	
	def getGood(self, good_name):
		for good in self.goods:
			if good.name == good_name:
				return good
		return None
	
	def setShopType(self, shop_type):
		self.shop_type = shop_type
	
	def getGoodById(self, good_id):
		for good in self.goods:
			if good.id == good_id:
				return good
		return None
	
	def getWorker(self, name, surname, sex):
		for worker in self.workers:
			if worker.name == name and worker.surname == surname and worker.sex == sex:
				return worker
		return None
	
	def getWorkerById(self, worker_id):
		for worker in self.workers:
			if worker.id_in_shop == worker_id:
				return worker
		return None
	
	def as_dict(self):
		return {
			'shop_id': self.shop_id,
			'name': self.name,
			'floor': self.floor,
			'shop_type': self.shop_type,
			'goods': [good.as_dict() for good in self.goods],
			'workers': [worker.as_dict() for worker in self.workers]
		}
