from classes import *
import stopit
import big_text

SHOW_INFO = False

@stopit.threading_timeoutable(default="intrat in timeout")
def bfs(gr, nrSolutiiCautate, fout=None):
    global SHOW_INFO
    #in coada vom avea doar noduri de tip NodParcurgere (nodurile din arborele de parcurgere)
    c=[NodParcurgere(gr.start, None, {}, 0, gr.calculeaza_h(None))]
    iteratie = 0

    while len(c)>0:
        # print("Coada actuala: " + str(c))
        #input()
        nodCurent=c.pop(0)
        iteratie += 1

        if SHOW_INFO:
            print(f'iteratie - {str(iteratie)}')
            print(f'f - {nodCurent.f}')
            print(f'g - {nodCurent.g}')
            print(str(nodCurent))

        if gr.testeaza_scop(nodCurent):
            print("Solutie:")
            nodCurent.afisDrum(afisCost=True, afisLung=True)
            print("\n----------------\n")

            if fout is not None:
                fout.write(big_text.solution)
                fout.write(nodCurent.strAfisDrum())

            nrSolutiiCautate-=1
            if nrSolutiiCautate==0:
                return nodCurent.getSolutionMoves()

        lSuccesori=gr.genereazaSuccesori(nodCurent)
        c.extend(lSuccesori)