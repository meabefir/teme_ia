import big_text
from classes import *
import heapq
import stopit
import time

@stopit.threading_timeoutable(default="intrat in timeout")
def a_star_opti(graph, nrOfSol, heuristic, fout=None):
    openSet = set()
    openHeap = []
    closedSet = set()
    start = time.time()

    first = NodParcurgere(graph.start, None, {}, 0, graph.calculeaza_h(None))
    openSet.add(first)
    openHeap.append((0, first))
    while openSet:
        current = heapq.heappop(openHeap)[1]

        graph.noduri_maxim = max(graph.noduri_maxim, len(openSet) + len(closedSet))

        if graph.testeaza_scop(current):
            print("Solutie: ")
            current.afisDrum(afisCost=True, afisLung=True)
            print("\n----------------\n")

            if fout is not None:
                fout.write(big_text.solution)
                fout.write(f"durata: {time.time() - start} sec \n")
                fout.write(f"nr noduri generate: {graph.noduri_generate} \n")
                fout.write(f"nr noduri maxim in memorie: {graph.noduri_maxim} \n")
                fout.write(current.strAfisDrum())

            return current.getSolutionMoves()

        openSet.remove(current)
        closedSet.add(current)

        listOfSuccessors = graph.genereazaSuccesori(current, heuristic)
        for tile in listOfSuccessors:
            if tile not in closedSet:
                if tile not in openSet:
                    openSet.add(tile)
                    heapq.heappush(openHeap, (tile.h, tile))
                tile.parent = current
    return []