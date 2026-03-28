## Execution Models

This experiment explores different Python execution strategies: **ThreadPool**, **ProcessPool**, and **InterpreterPool**.  
We benchmark them across **CPU**, **Memory**, **IO**, and **Network** workloads to understand performance, concurrency efficiency, and memory usage.

### Features

- Benchmark tasks with configurable number of workers and tasks  
- Generate performance plots (`wall time`, `CPU time`, `throughput`)  
- Evaluate concurrency metrics (`GIL efficiency`, `speedup`, `efficiency`)  
- Consolidate results into a Markdown report with machine specs  

### Folder Structure

```
.
├── bench.py                 # Run benchmark tests
├── consolidate.py           # Generate markdown report from results
├── executor_utils.py        # Utility functions for benchmark execution
├── plot.py                  # Plot benchmark results
├── workloads.py             # Definitions of benchmark workloads
├── config.json              # Benchmark configuration
├── Taskfile.yml             # Task definitions for automation
├── pyproject.toml           # Project dependencies
├── uv.lock                  # Dependency lock file
├── results/                 # Directory storing benchmark outputs
│   └── <timestamp>/         # Each run stored by timestamp
│       ├── plots/           # Plots for each metric
│       ├── report.md        # Consolidated markdown report
│       └── results.json     # Raw benchmark results
└── README.md                # Project documentation
```

### Getting Started

Available Tasks

The project uses [Task](https://taskfile.dev/) for automation. You can run the following tasks from the project root :

| Task        | Description                                              |
|------------|----------------------------------------------------------|
| `bench`     | Run benchmarks and generate plots (no report)             |
| `clean`     | Remove previous benchmark results                         |
| `consolidate` | Generate a markdown report from the latest run         |
| `dev`       | Format code, fix lint issues, and sort imports            |
| `format`    | Format code using Black                                   |
| `imports`   | Fix import ordering via Ruff                              |
| `lint`      | Run lint checks                                           |
| `lint-fix`  | Auto-fix lint issues (including imports)                  |
| `list`      | List previous benchmark runs                              |
| `plot`      | Plot the latest benchmark results                         |
| `run`       | Full pipeline: benchmark → plot → consolidate             |
| `setup`     | Create a virtual environment and install dependencies     |

Same list can be obtained by simply doing `task` from the project root.

### Usage

1. Setup Environment

```bash
task setup
```

2. Run Benchmarks

Run the benchmark for all workloads:

```bash
task bench
```

Or run the full pipeline (benchmark, plot then consolidate):

```bash
task run
```

3. View Results

- Plots are saved in : results/<timestamp>/plots/
- Raw results : results/<timestamp>/results.json
- Consolidated report : results/<timestamp>/report.md

4. Clean Up

```bash
task clean
```

>[!WARNING]
> Removes all previous benchmark results.

5. Development (code format, lint and import sorting)

```bash
task dev
```