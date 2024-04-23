class Good:
	def __init__(self, name, good_type):
		self.name = name
		self.good_type = good_type
		
		
	def as_dict(self):
		return {
			'name': self.name,
			'good_type':self.good_type
		}
