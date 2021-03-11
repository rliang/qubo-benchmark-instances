#!/usr/bin/env python3

from typing import TextIO
from io import BytesIO
from urllib.request import urlopen
from zipfile import ZipFile
from math import floor
import gzip
import multiprocessing


def orlib(n: int):
    gz = n >= 1000
    name = f"bqp{n}.{'gz' if gz else 'txt'}"
    print(name)

    def process(infile: TextIO):
        num = int(next(infile))
        for index in range(num):
            with open(f"bqp{n}.{index + 1}", "w") as outfile:
                _, nonzeros = map(int, next(infile).split())
                print(n, file=outfile)
                for i in range(nonzeros):
                    j, i, q = map(int, next(infile).split())
                    print(i - 1, j - 1, -q * (2 if j != i else 1), file=outfile)

    with urlopen(f"http://people.brunel.ac.uk/~mastjjb/jeb/orlib/files/{name}") as infile:
        if gz:
            with gzip.open(infile, mode="rt") as ingzip:
                process(ingzip)
        else:
            process(infile)


def palubeckis(n: int, index: int, density: int, seed: int):
    coef = float(2048 * 1024 * 1024 - 1)
    seed = float(seed)

    def random(seed: float):
        rd = seed * 16807
        seed = rd - floor(rd / coef) * coef
        return seed, seed / (coef + 1)

    print(f"p{n}.{index}")
    with open(f"p{n}.{index}", mode="w") as outfile:
        print(n, file=outfile)
        for i in range(n):
            seed, r = random(seed)
            print(i, i, -int(floor(r * 201.0 - 100.0)), file=outfile)
            for j in range(i + 1, n):
                seed, fl = random(seed)
                if fl * 100 <= density:
                    seed, r = random(seed)
                    print(j, i, -int(floor(r * 201.0 - 100.0)) * 2, file=outfile)


def stanford(index: int):
    print(f"G{index}")
    with urlopen(f"https://web.stanford.edu/~yyye/yyye/Gset/G{index}") as infile:
        n, nonzeros = map(int, next(infile).split())
        diag = [0] * n
        with open(f"G{index}", mode="w") as outfile:
            print(n, file=outfile)
            for _ in range(nonzeros):
                j, i, q = map(int, next(infile).split())
                diag[i - 1] -= q
                diag[j - 1] -= q
                print(i - 1, j - 1, q * 2, file=outfile)
            for i, q in enumerate(diag):
                print(i, i, q, file=outfile)


def optsicom():
    print(f"set2.zip")
    with urlopen(f"http://grafo.etsii.urjc.es/optsicom/maxcut/set2.zip") as inzip:
        with ZipFile(BytesIO(inzip.read())) as inzipfile:
            for name in inzipfile.namelist():
                with inzipfile.open(name) as infile:
                    n, nonzeros = map(int, next(infile).split())
                    diag = [0] * n
                    with open(name.split(".")[0], mode="w") as outfile:
                        print(n, file=outfile)
                        for _ in range(nonzeros):
                            j, i, q = map(int, next(infile).split())
                            diag[i - 1] -= q
                            diag[j - 1] -= q
                            print(i - 1, j - 1, q * 2, file=outfile)
                        for i, q in enumerate(diag):
                            print(i, i, q, file=outfile)


def dimacs(index: int):
    print(f"torus{index}")
    with urlopen(f"http://dimacs.rutgers.edu/archive/Challenges/Seventh/Instances/TORUS/torus{index}.dat.gz") as infile:
        with gzip.open(infile, mode="rt") as ingzip:
            n, nonzeros = map(int, next(ingzip).split())
            diag = [0] * n
            with open(f"torus{index}", mode="w") as outfile:
                print(n, file=outfile)
                for _ in range(nonzeros):
                    j, i, q = map(int, next(ingzip).split())
                    diag[i - 1] -= q
                    diag[j - 1] -= q
                    print(i - 1, j - 1, q * 2, file=outfile)
                for i, q in enumerate(diag):
                    print(i, i, q, file=outfile)



p = multiprocessing.Pool()
for n in [50, 100, 500, 1000, 2500]:
    p.apply_async(orlib, [n])
for n, density_seed in [
    (3000, [(50, 31000), (80, 32000), (80, 33000), (100, 34000), (100, 35000), (100, 36000)]),
    (4000, [(50, 41000), (80, 42000), (80, 43000), (100, 44000), (100, 45000), (100, 46000)]),
    (5000, [(50, 51000), (80, 52000), (80, 53000), (100, 54000), (100, 55000), (100, 56000)]),
    (6000, [(50, 61000), (80, 62000), (100, 64000)]),
    (7000, [(50, 71000), (80, 72000), (100, 74000)]),
]:
    for i, (density, seed) in enumerate(density_seed, 1):
        p.apply_async(palubeckis, [n, i, density, seed])
for i in [*range(1, 68), 70, 72, 77, 81]:
    p.apply_async(stanford, [i])
p.apply_async(optsicom)
for i in ["g3-8", "g3-15", "pm3-8-50", "pm3-15-50"]:
    p.apply_async(dimacs, [i])
p.close()
p.join()
