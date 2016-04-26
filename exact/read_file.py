from Graph import Graph
from Vertex import Vertex

def read_from_file(filepath):
	vertices = []
	with open(filepath) as file:
		line_cont = 1
		for line in file:
			if line_cont==1:
				line = line.split()
				name = line[1]
			elif line_cont>=6:
				line = line.split()
				if len(line)>0 and line[0]!='999':
					vertex = Vertex(label=line[0], 
						position=(float(line[1]), float(line[2])), 
						demand=float(line[3]),
						time_window=(float(line[4]), float(line[5])),
						service_time=float(line[6]))
					vertices.append(vertex)
			line_cont += 1
	graph = Graph(vertices)
	return graph

def from_google_maps():
	pass

if __name__=='__main__':
	read_from_file('n20w20.001.txt')
