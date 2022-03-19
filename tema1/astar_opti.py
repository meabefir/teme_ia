import big_text
from classes import *
import heapq
import stopit

@stopit.threading_timeoutable(default="intrat in timeout")
def a_star_opti(graph, nrOfSol, heuristic, fout=None):
    openSet = set()
    openHeap = []
    closedSet = set()

    def retracePath(c):
        path = [c]
        while c.parent is not None:
            c = c.parent
            path.append(c)
        path.reverse()
        return path

    first = NodParcurgere(graph.start, None, {}, 0, graph.calculeaza_h(None))
    openSet.add(first)
    openHeap.append((0, first))
    while openSet:
        current = heapq.heappop(openHeap)[1]

        if graph.testeaza_scop(current):
            print("Solutie: ")
            current.afisDrum(afisCost=True, afisLung=True)
            print("\n----------------\n")

            if fout is not None:
                fout.write(big_text.solution)
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