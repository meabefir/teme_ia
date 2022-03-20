import big_text
from classes import *
import stopit
import time

def dfi_aux(nodCurent, adancime, nrSolutiiCautate, gr, start, ret = None, fout = None):
	if adancime==1 and gr.testeaza_scop(nodCurent):
		print("Solutie: ", end="")
		nodCurent.afisDrum()
		print("\n----------------\n")

		gr.noduri_maxim = max(gr.noduri_maxim, adancime)

		if fout is not None:
			fout.write(big_text.solution)
			fout.write(f"durata: {time.time() - start} sec \n")
			fout.write(f"nr noduri generate: {gr.noduri_generate} \n")
			fout.write(f"nr noduri maxim in memorie: {gr.noduri_maxim} \n")
			fout.write(nodCurent.strAfisDrum())

		nrSolutiiCautate-=1
		if nrSolutiiCautate==0:
			return nrSolutiiCautate, nodCurent.getSolutionMoves()
	elif adancime>1:
		lSuccesori=gr.genereazaSuccesori(nodCurent)
		for sc in lSuccesori:
			if nrSolutiiCautate!=0:
				nrSolutiiCautate, ret =dfi_aux(sc, adancime-1, nrSolutiiCautate, gr, start, ret)
	return nrSolutiiCautate, ret

@stopit.threading_timeoutable(default="intrat in timeout")
def dfi(gr, nrSolutiiCautate=1, fout=None):
	start = time.time()
	ret = None
	for i in range(1, int(1e10)):
		if nrSolutiiCautate==0:
			return ret
		nrSolutiiCautate, ret =dfi_aux(NodParcurgere(gr.start, None, {}, 0, gr.calculeaza_h(None)), i, nrSolutiiCautate, gr, start, fout)
	return ret