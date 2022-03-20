import big_text
from classes import *
import stopit
import time


@stopit.threading_timeoutable(default="intrat in timeout")
def ida_star_noprint(gr, nrSolutiiCautate, tip_euristica="euristica admisibila 1", fout=None):
    nodStart =  NodParcurgere(gr.start, None, {}, 0, gr.calculeaza_h(gr.start))
    limita = nodStart.f
    start = time.time()

    while True:
        nrSolutiiCautate, rez = construieste_drum_noprint(gr, nodStart, limita, nrSolutiiCautate, tip_euristica, start, fout=fout)
        if rez == "gata":
            return nrSolutiiCautate
        if rez == float('inf'):
            break
        limita = rez


def construieste_drum_noprint(gr, nodCurent, limita, nrSolutiiCautate, tip_euristica, start, adancime=0, fout=None):
    gr.noduri_maxim = max(gr.noduri_maxim, adancime)
    if nodCurent.f > limita:
        return nrSolutiiCautate, nodCurent.f

    if gr.testeaza_scop(nodCurent) and nodCurent.f == limita:
        print("Solutie: ")
        nodCurent.afisDrum(afisCost=True, afisLung=True)
        print("limita ", limita)
        print("\n----------------\n")

        if fout is not None:
            fout.write(big_text.solution)
            fout.write(f"durata: {time.time() - start} sec \n")
            fout.write(f"nr noduri generate: {gr.noduri_generate} \n")
            fout.write(f"nr noduri maxim in memorie: {gr.noduri_maxim} \n")
            fout.write(nodCurent.strAfisDrum())

        nrSolutiiCautate -= 1
        if nrSolutiiCautate == 0:
            return nodCurent.getSolutionMoves(), "gata"

    lSuccesori = gr.genereazaSuccesori(nodCurent, tip_euristica)
    minim = float('inf')
    for s in lSuccesori:
        nrSolutiiCautate, rez = construieste_drum_noprint(gr, s, limita, nrSolutiiCautate, tip_euristica, start, adancime+1, fout)
        if rez == "gata":
            return nrSolutiiCautate, "gata"
        if rez < minim:
            minim = rez
    return nrSolutiiCautate, minim