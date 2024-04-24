class Worker:
	mall_id =1;
	def __init__(self, name, surname, shop_name, id_in_shop, sex, salary, position):
		self.id_in_shop = id_in_shop
		self.name = name
		self.surname = surname
		self.shop = shop_name
		self.mall_id = Worker.mall_id
		Worker.mall_id += 1
		self.sex = sex
		self.salary = salary
		self.position = position
	
	def as_dict(self):
		return {
			'name': self.name,
			'surname': self.surname,
			'shop': self.shop,
			'Mall_id': self.mall_id,
			'Id_in_shop': self.id_in_shop,
			'Sex': self.sex,
			'Salary': self.salary,
			'Position': self.position
		}
