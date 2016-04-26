class Vertex(object):
	"""A Vertex is a node in a graph."""

	def __init__(self, label='', position = (0, 0), demand = 0.0, time_window = (0.0, 0.0), service_time = 0.0):
		self.label = label
		self.position = position
		self.demand = demand
		self.time_window = time_window
		self.service_time = service_time

	def __repr__(self):
		"""Returns a string representation of this object that can
		be evaluated as a Python expression."""
		print_this = repr(self.label) + repr(self.position) + ". TW: " + repr(self.time_window) + "+" + repr(self.service_time) + ". Demand: " + repr(self.demand) 
		return 'Vertex(%s)' % print_this

	__str__ = __repr__
	"""The str and repr forms of this object are the same."""