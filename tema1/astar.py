import big_text
from classes import *
import stopit

@stopit.threading_timeoutable(default="intrat in timeout")
def a_star(graph, noOfSolutions, heuristic, fout=None):
    queue = [NodParcurgere(graph.start, None, {}, 0, graph.calculeaza_h(None))]

    while len(queue) > 0:
        currentNode = queue.pop(0)

        if graph.testeaza_scop(currentNode):
            print("Solutie: ")
            currentNode.afisDrum(afisCost=True, afisLung=True)
            print("\n----------------\n")

            if fout is not None:
                fout.write(big_text.solution)
                fout.write(currentNode.strAfisDrum())

            noOfSolutions -= 1
            if noOfSolutions == 0:
                return currentNode.getSolutionMoves()

        listOfSuccessors = graph.genereazaSuccesori(currentNode, heuristic)
        for s in listOfSuccessors:
            found = False
            for node in queue:
                if s.board == node.board:
                    found = True
                    break
            if found:
                continue
            i = 0
            found = False
            for i in range(len(queue)):
                if queue[i].f >= s.f or (queue[i].f == s.f and queue[i].g <= s.g):
                    found = True
                    break
            if found:
                queue.insert(i, s)
            else:
                queue.append(s)