1. Am folosit modulul argparse pt a parsa argumente primite in linia de comanda
  * -if -> input folder
  * -of -> output folder
  * -nsol -> soultions searched
  * -t -> timeout
- example use: python main.py -if input -of output -nsol 5 -t 10

2. Inputul este verificat inainte de a se contrui graf cu acesta
3. Metoda in clasa Graph. Itereaza toate piesele si incearca sa le miste in cele 4 directii
4. Metoda in clasa Piece.
5. Metoda in clasa Piece apelata pe piesa speciala care verifica daca este in afara tablei
6. * bana -> returneaza 1 mereu
   * admisibila 1 -> distanta manhattan
   * admisibila 2 -> exista cale libera pana la exit ? distanta_manhattan : distanta_manhattan + costul celei mai ieftin piese intalnite
   * neadmisibila -> prioritizeaza starile in care piesa are libertate de miscare
7. nu exista stare initiala care sa fie si finala. ar putea fi considerat cazul in care tabla pur si simplu nu contine piesa speciala, dar am ales sa il consider un caz invalid
   * input6 se blocheaza la dfs dar merge astar
   * input1 da solutie proasta pt euristica neadmisibila
8. merge
9. merge
10. * verifica corectitudine
   * nu prea merge sa realizezi ca nu are solutii, doar daca piesa speicala efectiv nu incape sa iasa, dar restul cazurilor sunt f greu de determinat (imposibil?)
   * optimizare mod de reprezentare eficient - momentan nu prea, tin si toata tabla pt fiecare nod dar si lista de piese, ar fi mai eficient daca as folosi doar lista de piese
   * găsirea unor condiții din care sa reiasă că o stare nu are cum sa contina in subarborele de succesori o stare finala - nu prea am cum, ar fi echivalentul cerintei b
   * pq si dictionare
11. merge
12. imi fac punctele cu interfata grafica :)
