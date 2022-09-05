from .poisson_disk import run_poisson

{'julia_cpu': [{'desired_samples': 1000, 'time_ms': 4.405545396730304}, {'desired_samples': 5000, 'time_ms': 21.63689660374075}, {'desired_samples': 10000,
                                                                                                                                  'time_ms': 44.12896779831499}, {'desired_samples': 50000, 'time_ms': 230.2900455892086}, {'desired_samples': 100000, 'time_ms': 244.81945021543652}]}


def benchmark():
    n_samples = [1000, 5000, 10000, 50000, 100000]
    results = []
    for n_sample in n_samples:
        print("Julia running", "n_sample", n_sample)
        results.append(run_poisson(n_sample))
        print("Done.")
    return {"julia_cpu": results}


if __name__ == "__main__":
    print(benchmark())
