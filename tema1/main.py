import sys
from argparse import ArgumentParser
import os
from classes import *

from dfs import dfs
from bfs import bfs
from dfi import dfi
from astar import a_star
from astar_opt import a_star_opt
from idastar import ida_star_noprint

import big_text

# python main.py -if input -of output -nsol 5 -t 5

def valid_input(s):
    """
        returneaza False, string_motiv daca inputul nu este corect
        returneaza True, "" daca validarea a fost successful
    """

    mat = [[ch for ch in row] for row in s.split('\n')]
    rows, cols = len(mat), len(mat[0])
    # nu are cum sa fie mai mica de 3x3
    if rows < 3 or cols < 3:
        return False, "too few rows or cols"
    # verific sa fie dreptunghiulara
    first_row_len = len(mat[0])
    for i in range(2,len(mat)):
        if len(mat[i]) != first_row_len:
            return False, "board is not rectangular"
    # verific daca contine piesa speciala
    found = False
    for row in mat:
        for ch in row:
            if ch == '*':
                found = True
    if not found:
        return False, "special piece not found"
    return True, ""

if __name__ == '__main__':
    parser = ArgumentParser()
    parser.add_argument('-if', '--ifolder', dest='input_folder', help='input folder path')
    parser.add_argument('-of', '--ofolder', dest='output_folder', help='output folder path')
    parser.add_argument('-nsol', dest='nsol', help='no solutions searched')
    parser.add_argument('-t', '--timeout', dest='timeout', help='The timeout for the searching algorithms')

    args = vars(parser.parse_args())
    input_folder, output_folder, nsol, timeout = args["input_folder"], args["output_folder"], int(args["nsol"]), int(args["timeout"])

    def solve_file(path, file_name):
        fin = open(path, 'r')
        content = fin.read()
        fin.close()

        is_valid, reason = valid_input(content)
        if not is_valid:
            fout = open(os.path.join(output_folder, "o_"+file_name), 'w')
            fout.write(f"Input file {file_name} does not have valid data\nReason: {reason}")
            fout.close()
            return
        else:
            alg_callbacks = {
                "dfs": dfs,
                "bfs": bfs,
                "dfi": dfi,
                "astar": a_star,
                "astar_opti": a_star_opt,
                "idastar": ida_star_noprint
            }
            fout = open(os.path.join(output_folder, "o_" + file_name), 'w', encoding="utf-8")
            algs = ["dfs", "bfs", "dfi", "astar", "astar_opti", "idastar"]
            heuristics = ["euristica banala", "euristica admisibila 1", "euristica neadmisibila 1"]
            for alg in algs:
                fout.write(alg+'\n')
                fout.write(big_text.algs[alg])
                if alg in ["dfs", "bfs", "dfi"]:
                    res = alg_callbacks[alg](Graph(path), nsol, timeout=timeout, fout=fout)
                    if isinstance(res, str):
                        fout.write(f"{alg} exceeded timeout\n")
                else:
                    for h in heuristics:
                        fout.write(big_text.heuristics[h])
                        res = alg_callbacks[alg](Graph(path), nsol, h, timeout=timeout, fout=fout)
                        if isinstance(res, str):
                            fout.write(f"{alg} exceeded timeout\n")
            fout.close()


    # creeaza folder de output daca nu exista deja
    if not os.path.isdir(output_folder):
        os.mkdir(output_folder)
    else:
        # sterge fisierele deja existente
        for file in os.listdir(output_folder):
            os.remove(os.path.join(output_folder, file))

    for file in os.listdir(input_folder):
        solve_file(os.path.join(input_folder, file), file)