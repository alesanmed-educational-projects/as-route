import copy

from Edge import Edge
from Graph import Graph
from Vertex import Vertex

def lopez_ibanez_blum_format(filepath):
	lines = [line.strip().split() for line in open(filepath, 'r')]
	N = int(lines[0][0])

	vertices = []
	vertices.append(Vertex('0')) #depot
	for i in range(1, N):
		vertices.append(Vertex(str(i)))

	# Read time windows
	vertices = []
	start_depot = None
	end_depot = None
	for i in range(len(lines[N+1:(2*N)+1])):
		line = lines[N+1:(2*N)+1][i]
		a = float(line[0])
		b = float(line[1])
		if i==0:
			start_depot = Vertex('start', (a, b))
			end_depot = Vertex('end', (a, b))
			vertices.append(start_depot)
		else:
			v = Vertex(str(i), (a, b))
			vertices.append(v)
	vertices.append(end_depot)

	# Read edges
	edges = []
	for i in range(len(lines[1:N+1])):
		line = lines[1:N+1][i]
		for j in range(len(line)):
			cost = float(line[j])
			if i!=j:
				e = Edge(vertices[i], vertices[j], cost)
				edges.append(e)
				if i==0:
					e = Edge(vertices[-1], vertices[j], cost)
					edges.append(e)
				if j==0:
					e = Edge(vertices[i], vertices[-1], cost)
					edges.append(e)
				
	return Graph(start_depot, end_depot, vertices, edges)			


def from_google_maps():
	pass

if __name__=='__main__':
	g = lopez_ibanez_blum_format('examples/n20w20.001.txt')