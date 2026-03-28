import os
import tempfile
import urllib.request


def cpu_heavy(n: int) -> int:
    s = 0
    for i in range(n):
        s += i * i
    return s


def memory_heavy(n: int) -> int:
    arr = [i for i in range(n)]
    return sum(arr)


def io_heavy(size_mb: int) -> int:
    data = "a" * (1024 * 1024)

    with tempfile.NamedTemporaryFile(delete=False) as tmp:
        filename = tmp.name
        for _ in range(size_mb):
            tmp.write(data.encode())

    total = 0
    with open(filename, "r") as f:
        for line in f:
            total += len(line)

    os.remove(filename)
    return total


def network_heavy(requests: int) -> int:
    total = 0
    for _ in range(requests):
        with urllib.request.urlopen("https://example.com") as r:
            total += len(r.read())
    return total


WORKLOADS = {
    "cpu": cpu_heavy,
    "memory": memory_heavy,
    "io": io_heavy,
    "network": network_heavy,
}
