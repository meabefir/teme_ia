
import queue
import heapq
from classes import *

show_info = False

def breadth_first(gr, nrSolutiiCautate):

	#in coada vom avea doar noduri de tip NodParcurgere (nodurile din arborele de parcurgere)
	c=[NodParcurgere(gr.start, None, {}, 0, gr.calculeaza_h(gr.start))]
	
	while len(c)>0:
		#print("Coada actuala: " + str(c))
		#input()
		nodCurent=c.pop(0)

		if gr.testeaza_scop(nodCurent):
			print("Solutie:")
			nodCurent.afisDrum(afisCost=True, afisLung=True)
			print("\n----------------\n")
			input()
			nrSolutiiCautate-=1
			if nrSolutiiCautate==0:
				return
		lSuccesori=gr.genereazaSuccesori(nodCurent)	
		c.extend(lSuccesori)

def a_star(gr, nrSolutiiCautate, tip_euristica):
	global show_info
	#in coada vom avea doar noduri de tip NodParcurgere (nodurile din arborele de parcurgere)
	q = queue.PriorityQueue()
	nod_start = NodParcurgere(gr.start, None, {}, 0, gr.calculeaza_h(gr.start))
	q.put(nod_start)
	open = {nod_start: nod_start}
	# q.queue va fi folosit pe post de open
	closed = {}
	iteratie = 0

	while not q.empty():
		iteratie += 1

		nodCurent = q.get()
		if not nodCurent in open:
			continue
		open.pop(nodCurent, None)
		closed[nodCurent] = nodCurent

		if show_info:
			print(f'iteratie - {str(iteratie)}\n')
			print(f'f - {nodCurent.f}\n')
			print(f'g - {nodCurent.g}\n')
			print(str(nodCurent))

		if gr.testeaza_scop(nodCurent):
			print("Solutie: ")
			nodCurent.afisDrum(afisCost=True, afisLung=True)
			print("\n----------------\n")
			# input()
			nrSolutiiCautate -= 1
			if nrSolutiiCautate == 0:
				return

		lSuccesori=gr.genereazaSuccesori(nodCurent, tip_euristica=tip_euristica)

		for s in lSuccesori:
			gasit = False

			if s in open:
				if s.f >= open[s].f:
					lSuccesori.remove(s)
				else:
					open.pop(s, None)

			# for nod_c in q.queue:
			# 	if nod_c.board == s.board:
			# 		gasit = True
			# 		if s.f >= nod_c.f:
			# 			lSuccesori.remove(s)
			# 		else:
			# 			q.queue.remove(nod_c)
			# 		break
			if not gasit:
				if s in closed:
					if s.f >= closed[s].f:
						lSuccesori.remove(s)
					else:
						closed.pop(s, None)

				# for nod_c in closed:
				# 	if s.board == nod_c.board:
				# 		if s.f >= nod_c.f:
				# 			lSuccesori.remove(s)
				# 		else:
				# 			closed.remove(nod_c)
				# 		break
		# am stricat stiva cand am scos direct din q.queue adica din open deci o repar
		# heapq.heapify(q.queue)

		for s in lSuccesori:
			q.put(s)
			open[s] = s

# gr=Graph("input0.txt")
# gr=Graph("input3.txt")
gr=Graph("input5.txt")

#Rezolvat cu breadth first
"""
print("Solutii obtinute cu breadth first:")
breadth_first(gr, nrSolutiiCautate=3)
"""
# breadth_first(gr, nrSolutiiCautate=1)

# a_star(gr, nrSolutiiCautate=3,tip_euristica="euristica admisibila 1")
# a_star(gr, nrSolutiiCautate=3, tip_euristica="euristica banala")
# a_star(gr, nrSolutiiCautate=1, tip_euristica="euristica banala")
# a_star(gr, nrSolutiiCautate=1, tip_euristica="euristica admisibila 1")
import cProfile
# cProfile.run('a_star(gr, nrSolutiiCautate=1, tip_euristica="euristica admisibila 5")')
a_star(gr, nrSolutiiCautate=1, tip_euristica="euristica admisibila 5")