from classes import *
import stopit
import big_text
import time

@stopit.threading_timeoutable(default="intrat in timeout")
def dfs(gr, nrSolutiiCautate=1, fout=None):
    stk = [NodParcurgere(gr.start, None, {}, 0, gr.calculeaza_h(None))]
    start = time.time()

    while len(stk):
        nodCurent = stk.pop(len(stk) - 1)
        if nrSolutiiCautate <= 0:
            return None
        gr.noduri_maxim = max(gr.noduri_maxim, len(stk))

        if gr.testeaza_scop(nodCurent):
            print("Solutie: ", end="")
            nodCurent.afisDrum()
            print("\n----------------\n")

            if fout is not None:
                fout.write(big_text.solution)
                fout.write(f"durata: {time.time() - start} sec \n")
                fout.write(f"nr noduri generate: {gr.noduri_generate} \n")
                fout.write(f"nr noduri maxim in memorie: {gr.noduri_maxim} \n")
                fout.write(nodCurent.strAfisDrum())

            nrSolutiiCautate -= 1
            if nrSolutiiCautate == 0:
                return nodCurent.getSolutionMoves()

        lSuccesori = gr.genereazaSuccesori(nodCurent)
        for sc in reversed(lSuccesori):
            if nrSolutiiCautate != 0:
                stk += [sc]