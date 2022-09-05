from .poisson_disk import run_poisson

{'numba_cpu': [{'desired_samples': 1000, 'time_ms': 8.600405813194811}, {'desired_samples': 5000, 'time_ms': 53.80218180362135}, {'desired_samples': 10000,
                                                                                                                                  'time_ms': 115.28392401523888}, {'desired_samples': 50000, 'time_ms': 637.3968123923987}, {'desired_samples': 100000, 'time_ms': 689.3348993966356}]}


def benchmark():
    n_samples = [1000, 5000, 10000, 50000, 100000]
    results = []
    for n_sample in n_samples:
        print("Numba running", "n_sample", n_sample)
        results.append(run_poisson(n_sample))
        print("Done.")
    return {"numba_cpu": results}


if __name__ == "__main__":
    print(benchmark())
