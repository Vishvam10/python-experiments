import os
import sys
import json
import time
import psutil

from concurrent.futures import ThreadPoolExecutor, ProcessPoolExecutor

try:
    from concurrent.futures import InterpreterPoolExecutor

    HAS_INTERPRETER = True
except ImportError:
    HAS_INTERPRETER = False

from executor_utils import run_task


def get_total_cpu_time():
    proc = psutil.Process(os.getpid())
    total = proc.cpu_times().user + proc.cpu_times().system

    for child in proc.children(recursive=True):
        try:
            t = child.cpu_times()
            total += t.user + t.system
        except Exception:
            pass

    return total


def get_memory_mb():
    return psutil.Process(os.getpid()).memory_info().rss / (1024 * 1024)


def gil_efficiency(cpu_time, wall_time, workers):
    if wall_time == 0:
        return 0
    return cpu_time / (wall_time * workers)


def simulate(executor, fn_name, arg, num_tasks, workers):
    cpu_before = get_total_cpu_time()
    wall_start = time.time()

    with executor(max_workers=workers) as ex:
        futures = [ex.submit(run_task, fn_name, arg) for _ in range(num_tasks)]
        _ = [f.result() for f in futures]

    wall_end = time.time()
    cpu_after = get_total_cpu_time()
    mem_after = get_memory_mb()

    wall = wall_end - wall_start
    cpu = cpu_after - cpu_before

    return {
        "wall_time": wall,
        "cpu_time": cpu,
        "throughput": num_tasks / wall,
        # NOTE : We are NOT using delta here as the Python GC sometimes 
        # asynchronously reclaims memory ... so sometimes it's negative
        "memory_mb": mem_after,
        "gil_eff": gil_efficiency(cpu, wall, workers),
    }


def benchmark(run_dir: str):
    with open("config.json") as f:
        CONFIG = json.load(f)

    base_path = os.path.join("results", run_dir)
    os.makedirs(base_path, exist_ok=True)

    strategies = {
        "ThreadPool": ThreadPoolExecutor,
        "ProcessPool": ProcessPoolExecutor,
    }

    if HAS_INTERPRETER:
        strategies["InterpreterPool"] = InterpreterPoolExecutor

    workers = 4
    num_tasks = 4

    results = {s: {} for s in strategies}

    for s_name, executor in strategies.items():
        for w_name in CONFIG:
            results[s_name][w_name] = {}

            for level, arg in CONFIG[w_name].items():
                print(f"{s_name} | {w_name} | {level}")

                baseline = simulate(ThreadPoolExecutor, w_name, arg, 1, 1)
                res = simulate(executor, w_name, arg, num_tasks, workers)

                res["speedup"] = baseline["wall_time"] / res["wall_time"]
                res["efficiency"] = res["speedup"] / workers

                results[s_name][w_name][level] = res

    out_file = os.path.join(base_path, "results.json")
    with open(out_file, "w") as f:
        json.dump(results, f, indent=4)

    print(f"\nSaved results to {out_file}")


if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage : python bench.py <RUN_DIR>")
        sys.exit(1)

    benchmark(sys.argv[1])
