import math

class Edge(object):
	"""An Edge is a tuple of two vertices."""

	def euclidean_distance(v1, v2):
		return math.hypot(v2[0] - v1[0], v2[1] - v1[1])

	def manhattan_distance(v1, v2):
		return math.fabs(v2[0] - v1[0]) + math.fabs(v2[1] - v1[1])

	def __init__(self, v1, v2, distance_function=euclidean_distance):
		"""The Edge constructor takes two vertices and a distance function."""
		self.v1 = v1
		self.v2 = v2
		self.cost = distance_function(self.v1.position, self.v2.position)
		self.time = self.cost

	def __repr__(self):
		"""Return a string representation of this object that can
		be evaluated as a Python expression."""
		print_this = "[" + repr(self.v1.label) + ", " + repr(self.v2.label) + "] = " + repr(self.cost)
		return 'Edge(%s)' % print_this

	__str__ = __repr__
	"""The str and repr forms of this object are the same."""