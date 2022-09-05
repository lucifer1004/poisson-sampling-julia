import matplotlib.pyplot as plt
import sys
import os

from src.taichi.benchmark import benchmark as benchmark_taichi
from src.julia.benchmark import benchmark as benchmark_julia
from src.numba.benchmark import benchmark as benchmark_numba

numba_sample_results = {'numba_cpu': [{'desired_samples': 1000, 'time_ms': 8.600405813194811}, {'desired_samples': 5000, 'time_ms': 53.80218180362135}, {'desired_samples': 10000,
                                                                                                                                                         'time_ms': 115.28392401523888}, {'desired_samples': 50000, 'time_ms': 637.3968123923987}, {'desired_samples': 100000, 'time_ms': 689.3348993966356}]}

taichi_sample_results = {'taichi_cpu': [{'desired_samples': 1000, 'time_ms': 16.961263469420373}, {'desired_samples': 5000, 'time_ms': 88.96173246515295}, {
    'desired_samples': 10000, 'time_ms': 166.0814554663375}, {'desired_samples': 50000, 'time_ms': 832.8834265936166}, {'desired_samples': 100000, 'time_ms': 892.8499184704075}]}

julia_sample_results = {'julia_cpu': [{'desired_samples': 1000, 'time_ms': 4.405545396730304}, {'desired_samples': 5000, 'time_ms': 21.63689660374075}, {
    'desired_samples': 10000, 'time_ms': 44.12896779831499}, {'desired_samples': 50000, 'time_ms': 230.2900455892086}, {'desired_samples': 100000, 'time_ms': 244.81945021543652}]}


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
