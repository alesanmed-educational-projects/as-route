import math

class Edge(object):
	"""An Edge is a tuple of two vertices."""

	def euclidean_distance(self, v1, v2):
		return math.hypot(v2.position[0] - v1.position[0], v2.position[1] - v1.position[1])

	def manhattan_distance(self, v1, v2):
		return math.fabs(v2.position[0] - v1.position[0]) + math.fabs(v2.position[1] - v1.position[1])

	def __init__(self, v1, v2, time):
		"""The Edge constructor takes two vertices and a distance function."""
		self.v1 = v1
		self.v2 = v2
		if v1.label=='start' and v2.label=='end':
			self.time = time
		else:
			self.time = self.euclidean_distance(v1, v2)

	def __repr__(self):
		"""Return a string representation of this object that can
		be evaluated as a Python expression."""
		print_this = "[" + repr(self.v1.label) + ", " + repr(self.v2.label) + "] = " + repr(self.time)
		return 'Edge(%s)' % print_this

	__str__ = __repr__
	"""The str and repr forms of this object are the same."""