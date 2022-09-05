from .poisson_disk import run_poisson

{'taichi_cpu': [{'desired_samples': 1000, 'time_ms': 16.961263469420373}, {'desired_samples': 5000, 'time_ms': 88.96173246515295}, {'desired_samples': 10000,
                                                                                                                                    'time_ms': 166.0814554663375}, {'desired_samples': 50000, 'time_ms': 832.8834265936166}, {'desired_samples': 100000, 'time_ms': 892.8499184704075}]}

def benchmark():
    n_samples = [1000, 5000, 10000, 50000, 100000]
    results = []
    for n_sample in n_samples:
        print("CPU running", "n_sample", n_sample)
        results.append(run_poisson(n_sample))
        print("Done.")
    return {"taichi_cpu": results}


if __name__ == "__main__":
    print(benchmark())
