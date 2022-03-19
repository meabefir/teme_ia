from classes import *
import stopit

SHOW_INFO = False

@stopit.threading_timeoutable(default="intrat in timeout")
def a_star_opt(gr, nrSolutiiCautate, tip_euristica, fout=None):
    global SHOW_INFO
    l_open = [NodParcurgere(gr.start, None, {}, 0, gr.calculeaza_h(None))]
    l_closed = []
    iteratie = 0
    while len(l_open) > 0:
        nodCurent = l_open.pop(0)
        l_closed.append(nodCurent)

        if SHOW_INFO:
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
                return nodCurent.getSolutionMoves()

        lSuccesori = gr.genereazaSuccesori(nodCurent, tip_euristica=tip_euristica)
        for s in lSuccesori:
            gasitC = False
            for nodO in l_open:
                if s.info == nodO.info:
                    gasitC = True
                    if s.f >= nodO.f:
                        lSuccesori.remove(s)
                    else:  # s.f<nodC.f
                        l_open.remove(nodO)
                    break
            if not gasitC:
                for nodC in l_closed:
                    if s.info == nodC.info:
                        if s.f >= nodC.f:
                            lSuccesori.remove(s)
                        else:  # s.f<nodC.f
                            l_closed.remove(nodC)
                        break
        for s in lSuccesori:
            i = 0
            gasit_loc = False
            for i in range(len(l_open)):
                # diferenta fata de UCS e ca ordonez crescator dupa f
                # daca f-urile sunt egale ordonez descrescator dupa g
                if l_open[i].f > s.f or (l_open[i].f == s.f and l_open[i].g <= s.g):
                    gasit_loc = True
                    break
            if gasit_loc:
                l_open.insert(i, s)
            else:
                l_open.append(s)