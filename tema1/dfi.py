import big_text
from classes import *
import stopit

def dfi_aux(nodCurent, adancime, nrSolutiiCautate, gr, ret = None, fout = None):
	if adancime==1 and gr.testeaza_scop(nodCurent):
		print("Solutie: ", end="")
		nodCurent.afisDrum()
		print("\n----------------\n")

		if fout is not None:
			fout.write(big_text.solution)
			fout.write(nodCurent.strAfisDrum())

		nrSolutiiCautate-=1
		if nrSolutiiCautate==0:
			return nrSolutiiCautate, nodCurent.getSolutionMoves()
	elif adancime>1:
		lSuccesori=gr.genereazaSuccesori(nodCurent)
		for sc in lSuccesori:
			if nrSolutiiCautate!=0:
				nrSolutiiCautate, ret =dfi_aux(sc, adancime-1, nrSolutiiCautate, gr, ret)
	return nrSolutiiCautate, ret

@stopit.threading_timeoutable(default="intrat in timeout")
def dfi(gr, nrSolutiiCautate=1, fout=None):
	ret = None
	for i in range(1, int(1e10)):
		if nrSolutiiCautate==0:
			return ret
		nrSolutiiCautate, ret =dfi_aux(NodParcurgere(gr.start, None, {}, 0, gr.calculeaza_h(None)), i, nrSolutiiCautate, gr, fout)
	return ret