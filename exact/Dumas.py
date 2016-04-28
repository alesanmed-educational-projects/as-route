from operator import attrgetter
from Solution import Solution
from read_file import silva_urrutia_format

from Graph import Graph

class Dumas(object):
	"""Problem implementation"""

	def __init__(self, graph):
		self.graph = graph

	def __repr__(self):
		n_vertices = len(self.graph.vertices())
		n_edges = len(self.graph.edges())
		print_this = "N_vertices: " + str(n_vertices) + ". E_edges: " + str(n_edges)
		return 'Dumas(%s)' % print_this

	def f(self, S, j):
		"""
		Dumas exact algorithm for the TSPTW
		Literature: http://pubsonline.informs.org/doi/pdf/10.1287/opre.43.2.367

		In:
			S: Subset of unvisited nodes of the solution
			j: Final node of path. Contained in S.

		Out:
			End time t of a path starting at depot node, 
			passing through every node in S exactly once, 
			ending at node j (contained in S).
		"""

		if len(S)==2:
			print("Caso base: " + str(S) + ", j=" + str(j))
			print("es " + str(self.base_case(S, j).total_cost()))
			print("factible : " + str(self.base_case(S, j).is_feasible()))
			return self.base_case(S, j)
		else:
			S.remove(j)
			print("Nuevo S: " + str(S))
			print()
			feasible_solutions = []
			for i in S:
				#ESTA es la zona wapa
				if i!=self.graph.start:
					t_ij = self.graph.time_edge(i,j)
					s_i = i.service_time

					solution = self.f(S, i)
					if solution:
						t_i = solution.last_time()
					else:
						# if None then no solutions feasibles
						continue

					a_j = j.time_window[0]

					t_j = max([t_i + s_i + t_ij, a_j])

					solution.add_vertex(j, t_j)

					if len(solution.vertices)==4:
						print("AQUI")
						print(solution)


					'''print()
					print("Para el i=" + str(i))
					print("Para el j=" + str(j))
					print("(a_i, b_i): " + str((a_i, b_i)))
					print("t_i: " + str(t_i))
					print("s_i+t_ij: " + str(s_i + t_ij))
					print("(a_j, b_j): " + str((a_j, b_j)))
					print("t_j: " + str(t_j))'''

					if solution.is_feasible():
						feasible_solutions.append(solution)
			return self.choose_sol(feasible_solutions)

	def choose_sol(self, solutions):
		if len(solutions)==0:
			"No hay soluciones factibles"
			return None
		else:
			return min(solutions, key=attrgetter('cost'))

	def base_case(self, S, j):
		"""
		Base case.
			f({1,j}, j) = tj      if (1,j) in E (edges)
			f({1,j}, j) = Inf     otherwise
		where
			a_j <= t_j <= b_j
			and
			t_j = max {a_1 + s_1 + t_ij, a_j}
		"""

		solution = Solution(self.graph, self.graph.start)

		a_1 = self.graph.start.time_window[0]
		s_1 = self.graph.start.service_time
		t_1j = self.graph.time_edge(self.graph.start, j)
		a_j = j.time_window[0]
		t_j = max([a_1 + s_1 + t_1j, a_j])

		solution.add_vertex(j, t_j)
		return solution

if __name__=='__main__':
	graph = silva_urrutia_format('n20w20.001_small.txt')

	dumas = Dumas(graph)
	S = list(dumas.graph.vertices())

	end = dumas.graph.end

	print("S: " + str(S))
	print()
	print()
	print("-----------")
	r = dumas.f(S, end)

	print()
	print()
	print("-----------")
	print(r)