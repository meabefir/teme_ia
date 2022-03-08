
import queue
import heapq
from classes import *

show_info = False

def breadth_first(gr, nrSolutiiCautate):

	#in coada vom avea doar noduri de tip NodParcurgere (nodurile din arborele de parcurgere)
	c=[NodParcurgere(gr.start, None)]
	
	while len(c)>0:
		#print("Coada actuala: " + str(c))
		#input()
		nodCurent=c.pop(0)

		if gr.testeaza_scop(nodCurent):
			print("Solutie:")
			# nodCurent.afisDrum(afisCost=True, afisLung=True)
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
	q.put(NodParcurgere(gr.start, None, {}, 0, gr.calculeaza_h(gr.start)))
	# q.queue va fi folosit pe post de open
	l_closed = []
	iteratie = 0

	while not q.empty():
		iteratie += 1

		nodCurent = q.get()
		if show_info:
			print(f'iteratie - {str(iteratie)}\n')
			print(f'f - {nodCurent.f}\n')
			print(f'g - {nodCurent.g}\n')
			print(str(nodCurent))
		if gr.testeaza_scop(nodCurent):
			print("Solutie: ")
			nodCurent.afisDrum(afisCost=True, afisLung=True)
			print("\n----------------\n")
			input()
			nrSolutiiCautate -= 1
			if nrSolutiiCautate == 0:
				return

		lSuccesori=gr.genereazaSuccesori(nodCurent, tip_euristica=tip_euristica)

		for s in lSuccesori:
			gasit = False
			for nod_c in q.queue:
				if nod_c.board == s.board:
					gasit = True
					if s.f >= nod_c.f:
						lSuccesori.remove(s)
					else:
						q.queue.remove(nod_c)
					break
			if not gasit:
				for nod_c in l_closed:
					if s.board == nod_c.board:
						if s.f >= nod_c.f:
							lSuccesori.remove(s)
						else:
							l_closed.remove(nod_c)
						break
		# am stricat stiva cand am scos direct din q.queue adica din open deci o repar
		heapq.heapify(q.queue)

		for s in lSuccesori:
			q.put(s)

gr=Graph("input3.txt")

#Rezolvat cu breadth first
"""
print("Solutii obtinute cu breadth first:")
breadth_first(gr, nrSolutiiCautate=3)
"""

nrSolutiiCautate=3
# a_star(gr, nrSolutiiCautate=3,tip_euristica="euristica admisibila 1")
# a_star(gr, nrSolutiiCautate=3, tip_euristica="euristica banala")
a_star(gr, nrSolutiiCautate=1, tip_euristica="euristica admisibila 3")
# a_star(gr, nrSolutiiCautate=1, tip_euristica="euristica banala")
