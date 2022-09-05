import matplotlib.pyplot as plt
import sys
import os

from src.taichi.benchmark import benchmark as benchmark_taichi
from src.julia.benchmark import benchmark as benchmark_julia
from src.numba.benchmark import benchmark as benchmark_numba

numba_sample_results = {'numba_cpu': [{'desired_samples': 1000, 'time_ms': 8.729429193772376}, {'desired_samples': 5000, 'time_ms': 54.30453319568187}, {
    'desired_samples': 10000, 'time_ms': 114.32691961526871}, {'desired_samples': 50000, 'time_ms': 638.4390128077939}, {'desired_samples': 100000, 'time_ms': 682.2548018069938}]}

taichi_sample_results = {'taichi_cpu': [{'desired_samples': 1000, 'time_ms': 16.892206738702953}, {'desired_samples': 5000, 'time_ms': 83.55948373985787}, {
    'desired_samples': 10000, 'time_ms': 167.95633606767905}, {'desired_samples': 50000, 'time_ms': 841.8607126067703}, {'desired_samples': 100000, 'time_ms': 905.9399942712238}]}

julia_sample_results = {'julia_cpu': [{'desired_samples': 1000, 'time_ms': 4.350052401423454}, {'desired_samples': 5000, 'time_ms': 21.523955394513905}, {
    'desired_samples': 10000, 'time_ms': 46.494469000026584}, {'desired_samples': 50000, 'time_ms': 228.63133139908314}, {'desired_samples': 100000, 'time_ms': 246.3819775963202}]}


def run_benchmarks():
    return benchmark_julia(), benchmark_numba(), benchmark_taichi()


def extract_perf(results):
    perf = []
    for record in results:
        perf.append(record["time_ms"])
    return perf


def extract_samples(results):
    samples = []
    for record in results:
        samples.append(record["desired_samples"])
    return samples


def plot_bar(julia_results, numba_results, taichi_results):
    fig, ax = plt.subplots(figsize=(6, 4))

    x_taichi = extract_samples(taichi_results["taichi_cpu"])
    y_taichi = extract_perf(taichi_results["taichi_cpu"])
    x_numba = extract_samples(numba_results["numba_cpu"])
    y_numba = extract_perf(numba_results["numba_cpu"])
    x_julia = extract_samples(julia_results["julia_cpu"])
    y_julia = extract_perf(julia_results["julia_cpu"])

    labels = ["{}".format(i) for i in x_taichi]

    # series
    bar_pos = [i * 4 for i in range(len(x_taichi))]
    ax.bar(bar_pos, y_taichi)

    bar_pos = [i * 4 + 1 for i in range(len(x_numba))]
    ax.bar(bar_pos, y_numba)

    bar_pos = [i * 4 + 2 for i in range(len(x_julia))]
    ax.bar(bar_pos, y_julia)

    bar_pos_ticks = [i * 4 + 1 for i in range(len(x_taichi))]
    ax.set_xticks(bar_pos_ticks, labels)

    plt.yscale("log")
    plt.grid('minor', axis='y')
    plt.xlabel("Samples")
    plt.ylabel("Execution time in ms")
    plt.legend([
        "Taichi",
        "Numba",
        "julia",
    ],
        loc='upper left')
    plt.title("Poisson Disk Sampling")
    plt.savefig("fig/bench.png", dpi=150)


if __name__ == '__main__':
    try:
        os.makedirs('fig')
    except FileExistsError:
        pass
    if len(sys.argv) >= 2 and sys.argv[1] == "sample":
        plot_bar(julia_sample_results, numba_sample_results,
                 taichi_sample_results)
    else:
        julia_sample_results, numba_sample_results, taichi_sample_results = run_benchmarks()
        print(julia_sample_results)
        print(numba_sample_results)
        print(taichi_sample_results)
