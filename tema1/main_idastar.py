
from classes import *


def ida_star(gr, nrSolutiiCautate, tip_euristica):
    nodStart =  NodParcurgere(gr.start, None, {}, 0, gr.calculeaza_h(gr.start))
    limita = nodStart.f
    while True:

        print("Limita de pornire: ", limita)
        nrSolutiiCautate, rez = construieste_drum(gr, nodStart, limita, nrSolutiiCautate, tip_euristica)
        if rez == "gata":
            break
        if rez == float('inf'):
            print("Nu mai exista solutii!")
            break
        limita = rez
        print(">>> Limita noua: ", limita)


def construieste_drum(gr, nodCurent, limita, nrSolutiiCautate, tip_euristica):
    print(nodCurent.info['*'].getBB())
    print(nodCurent.info['*'].isOOB())
    print("A ajuns la: ", nodCurent)
    if nodCurent.f > limita:
        print("returning, trece de limita")
        return nrSolutiiCautate, nodCurent.f

    # if gr.testeaza_scop(nodCurent) and nodCurent.f == limita:
    if gr.testeaza_scop(nodCurent):
        print("Solutie: ")
        nodCurent.afisDrum()
        print(limita)
        print(nodCurent.g)
        print("\n----------------\n")
        nrSolutiiCautate -= 1
        if nrSolutiiCautate == 0:
            return 0, "gata"
    print("-------------------------------------")

    lSuccesori = gr.genereazaSuccesori(nodCurent, tip_euristica)
    minim = float('inf')
    for s in lSuccesori:
        nrSolutiiCautate, rez = construieste_drum(gr, s, limita, nrSolutiiCautate, tip_euristica)
        if rez == "gata":
            return 0, "gata"
        print("Compara ", rez, " cu ", minim)
        if rez < minim:
            minim = rez
            print("Noul minim: ", minim)
    return nrSolutiiCautate, minim

it = 0
def ida_star_noprint(gr, nrSolutiiCautate, tip_euristica):
    nodStart =  NodParcurgere(gr.start, None, {}, 0, gr.calculeaza_h(gr.start))
    limita = nodStart.f
    while True:

        # print("Limita de pornire: ", limita)
        nrSolutiiCautate, rez = construieste_drum_noprint(gr, nodStart, limita, nrSolutiiCautate, tip_euristica)
        if rez == "gata":
            break
        if rez == float('inf'):
            # print("Nu mai exista solutii!")
            break
        limita = rez
        # print(">>> Limita noua: ", limita)


def construieste_drum_noprint(gr, nodCurent, limita, nrSolutiiCautate, tip_euristica):
    # print(nodCurent.info['*'].getBB())
    # print(nodCurent.info['*'].isOOB())
    # print("A ajuns la: ", nodCurent)
    global it
    it += 1
    if nodCurent.f > limita:
        # print("returning, trece de limita")
        return nrSolutiiCautate, nodCurent.f

    if gr.testeaza_scop(nodCurent) and nodCurent.f == limita:
    # if gr.testeaza_scop(nodCurent):
        print("Solutie: ")
        nodCurent.afisDrum()
        print(limita)
        print(nodCurent.g)
        print("\n----------------\n")
        nrSolutiiCautate -= 1
        if nrSolutiiCautate == 0:
            return 0, "gata"
    # print("-------------------------------------")

    lSuccesori = gr.genereazaSuccesori(nodCurent, tip_euristica)
    minim = float('inf')
    for s in lSuccesori:
        nrSolutiiCautate, rez = construieste_drum_noprint(gr, s, limita, nrSolutiiCautate, tip_euristica)
        if rez == "gata":
            return 0, "gata"
        # print("Compara ", rez, " cu ", minim)
        if rez < minim:
            minim = rez
            # print("Noul minim: ", minim)
    return nrSolutiiCautate, minim

gr = Graph("input4.txt")

# Rezolvat cu breadth first
"""
print("Solutii obtinute cu breadth first:")
breadth_first(gr, nrSolutiiCautate=3)
"""

nrSolutiiCautate = 3
# a_star(gr, nrSolutiiCautate=3,tip_euristica="euristica admisibila 1")
# a_star(gr, nrSolutiiCautate=3, tip_euristica="euristica banala")
# a_star(gr, nrSolutiiCautate=3, tip_euristica="euristica admisibila 1")
# ida_star(gr, nrSolutiiCautate=3, tip_euristica="euristica admisibila 1")
ida_star_noprint(gr, nrSolutiiCautate=1, tip_euristica="euristica admisibila 1")
print(f'iteratii {it}')
