from juliacall import Main as jl
from os.path import join, abspath, dirname

jl.include(join(dirname(abspath(__file__)), '..',
           '..', '..', 'src', 'poisson_2d.jl'))


def run_poisson(desired_samples=100000):
    grid = (400, 400)

    def run():
        import time
        jl.sample_2d(grid, desired_samples)
        repeats = 5

        t = time.perf_counter()
        for _ in range(repeats):
            jl.sample_2d(grid, desired_samples)
        avg_time_ms = (time.perf_counter() - t) / repeats * 1000
        return {'desired_samples': desired_samples, 'time_ms': avg_time_ms}
    return run()
