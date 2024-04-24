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
		
	def addGood(self, good_name, good_type):
		self.goods.append(good.Good(good_name, good_type, self.good_id))
		self.good_id +=1
		
	def addWorker(self, name, surname, sex, position, salary):
		self.workers.append(worker.Worker(name, surname, self.name, self.worker_id, sex, position, salary))
		self.worker_id += 1
		
	def as_dict(self):
		return {
			'shop_id': self.shop_id,
			'name': self.name,
			'floor': self.floor,
			'goods': [good.as_dict() for good in self.goods],
			'workers': [worker.as_dict() for worker in self.workers]
		}
