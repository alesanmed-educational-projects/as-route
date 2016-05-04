import matplotlib.pyplot as plt
import time

from exact.Dumas import Dumas
from exact.read_file import lopez_ibanez_blum_format

def time_exact(n):
	t = time.time()
	graph = lopez_ibanez_blum_format('exact/examples/n20w'+str(n)+'.001.txt')
	dumas = Dumas(graph)
	solution = dumas.run()
	return time.time() - t

def time_heuristic(n):
	#TODO
	return 5

def run():
	N_values = list(range(10, 15))
	times_exact = []
	times_heur = []
	for n in N_values:
		times_exact.append(time_exact(n))
		times_heur.append(time_heuristic(n))

	plt.plot(N_values, times_exact)
	plt.plot(N_values, times_heur)
	plt.legend(['Dumas', 'TPH'], loc='upper left')
	plt.show()

if __name__=="__main__":
	run()

		

