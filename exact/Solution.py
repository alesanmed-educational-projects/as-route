
class Solution(object):
	def __init__(self, graph, depot, time=0.0):
		self.graph = graph
		self.vertices = [depot]
		self.times = [0.0]
		
	def __repr__(self):
		print_this = repr(self.vertices)
		return 'Solution(%s)' % print_this

	__str__=__repr__

	def add_vertex(self, vertex, time):
		self.vertices.append(vertex)
		self.times.append(time)
		self.cost = self.total_cost()

	def total_cost(self):
		t_ij = 0
		for first, second in zip(self.vertices, self.vertices[1:]):
			t_ij += self.graph.time_edge(first, second)
		return t_ij

	def last_time(self):
		return self.times[-1]

	def is_feasible(self):
		result = True

		cont = 0
		for first, second in zip(self.vertices, self.vertices[1:]):
			t_ij = self.graph.time_edge(first, second)
			s_i = first.service_time
			t_i = self.times[cont]
			t_j = self.times[cont+1]
			result = result and t_j>=t_i+s_i+t_ij
			cont += 1

		for i in range(0, len(self.times)):
			t_i = self.times[i]
			vertex = self.vertices[i]
			a_i = vertex.time_window[0]
			b_i = vertex.time_window[1]
			result = result and a_i<=t_i and t_i<=b_i

		return result
