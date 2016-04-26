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

	

if __name__=='__main__':
	graph = read_from_file('n20w20.001.txt')
	dumas = Dumas(graph)
	print(dumas)