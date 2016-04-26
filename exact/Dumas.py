from read_file import read_from_file

class Dumas(object):
	"""Problem implementation"""

	def __init__(self, graph):
		self.graph = graph

	def __repr__(self):
		n_vertices = len(self.graph.vertices())
		n_edges = len(self.graph.edges())
		print_this = "N_vertices: " + str(n_vertices) + ". E_edges: " + str(n_edges)
		return 'Dumas(%s)' % print_this

	def f(S, i, t_i):
		"""
		Dumas exact algorithm for the TSPTW
		Literature: http://pubsonline.informs.org/doi/pdf/10.1287/opre.43.2.367

		In:
			S: Subset of unvisited nodes of the solution
			j: Final node of path. Contained in S.
			t_i: Time of arriving at j.

		Out:
			Least cost of a path starting at depot node, 
			passing through every node in S exactly once, 
			ending at node j (contained in S),
			and ready to service node j at time t or later.
		"""

		if len(S)==2:
			return self.base_case(S, i, t)
		else:
			s = S.remove(i)
			solutions = []
			for j in s:
				t_j = self.t_j(i, j, t_i)
				if self.time_restrictions(i, j, t_i, t_j):
					c_ij = self.graph.cost_edge(i,j)
					solutions.append(f(s, j, t_j) + c_ij)
			return min(solutions)

	def base_case(self, S, j, t):
		return self.graph.cost_edge(S[0],S[1])

	def t_j(self, i, j, t_i):
		"""
		If a path goes from nodes i to j
		and passes by node i at t_i,
		the time service begins at node j is given by
		t_j = max ( t_i + s_i + t_ij, a_j)

		where
			t_i : time service beginning at node i.
			s_i : time service duration of node i.
			t_ij : time cost of travelling i->j.
			a_j : ready time of node j.
		"""
		s_i = i.service_time
		t_ij = self.graph.time_edge(i,j)
		a_j = j.time_window[0]
		return max([t_i + s_i + t_ij, a_j])

	def time_restrictions(self, i, j, t_i, t_j):
		t_j >=t_i + s_j + t_ij
		t_ij = self.graph.time_edge(i,j)

		r1 = t_j >= t_i + s_i + t_ij
		r2 = j.time_window[0] <= t_j and t_j <= j.time_window[1]
		return r1 and r2

	

if __name__=='__main__':
	graph = read_from_file('n20w20.001.txt')
	dumas = Dumas(graph)
	print(dumas)