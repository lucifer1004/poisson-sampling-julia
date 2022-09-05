# Poisson Disk Sampling Benchmark

## Introduction
In this benchmark, we compare three Poisson Disk Sampling implementations among
Taichi, Numba, and Julia.
The algorithm is suitable for single-threaded performance comparisons.
<p align="center">
<img src="fig/demo.gif" height="370px" />
</p>

## Evaluation

Performance is measured in milliseconds (ms), we run over different
number of samples.
The reported times are measured using a 400 x 400 grid. 
The employed Taichi version 
is [1.1.2](https://github.com/taichi-dev/taichi/releases/tag/v1.1.2), 
the Numpy version is 1.23.2, the Numba version is 0.56.2, the 
Python version is 3.9.12, and the Julia version is 1.8.0.

<p align="center">
<img src="fig/bench.png" width="600">
</p>

## Reproduction Steps

* Pre-requisites
```shell
python3 -m pip install numpy numba
python3 -m pip install taichi
python3 -m pip install matplotlib
python3 -m pip install juliacall
```
* Run the benchmark and draw the plots
```shell
python3 plot_benchmark.py
```
