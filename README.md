# qubo-benchmark-instances
A script for downloading benchmark instances of the QUBO problem.

## Usage

```sh
wget -O- https://raw.githubusercontent.com/rliang/qubo-benchmark-instances/main/get.py | python3 --
```

This will retrieve the instances to the current directory,
one per file.

## Output format

The direction of optimization is assumed to be minimization,
and the matrices are in lower-triangular form.

* The first line contains `n`.
* Each subsequent line until the end of the file contains `i j Qij`, where j <= i.

## Instance sets

* [ORLib](http://people.brunel.ac.uk/~mastjjb/jeb/orlib/files)
* [Palubeckis](https://www.personalas.ktu.lt/~ginpalu)
* [Stanford Gset](https://web.stanford.edu/~yyye/yyye/Gset) (reduced from Max-Cut)
* [Optsicom Set2](http://grafo.etsii.urjc.es/optsicom/maxcut) (reduced from Max-Cut)
* [DIMACS](http://dimacs.rutgers.edu/archive/Challenges/Seventh/Instances) (reduced from Max-Cut)
