class Good:
	def __init__(self, name, good_type, good_id):
		self.name = name
		self.good_type = good_type
		self.good_id = good_id
		
	def as_dict(self):
		return {
			'name': self.name,
			'good_type':self.good_type,
			'good_id': self.good_id
		}
