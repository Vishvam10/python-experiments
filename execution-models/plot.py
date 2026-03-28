import os
import sys
import json
import numpy as np
import matplotlib as mpl
import matplotlib.pyplot as plt
import catppuccin


# -------------------------
# Style
# -------------------------

mpl.style.use(catppuccin.PALETTE.macchiato.identifier)

STRATEGY_COLORS = {
    "ThreadPool": catppuccin.PALETTE.macchiato.colors.red.hex,
    "ProcessPool": catppuccin.PALETTE.macchiato.colors.blue.hex,
    "InterpreterPool": catppuccin.PALETTE.macchiato.colors.green.hex,
}


# -------------------------
# Load
# -------------------------

if len(sys.argv) < 2:
    print("Usage : python plot.py <RUN_DIR>")
    sys.exit(1)

run_dir = sys.argv[1]

base_path = os.path.join("results", run_dir)
results_file = os.path.join(base_path, "results.json")
plots_dir = os.path.join(base_path, "plots")

os.makedirs(plots_dir, exist_ok=True)

with open(results_file, "r") as f:
    results = json.load(f)


# -------------------------
# Config
# -------------------------

levels = ["low", "med", "high"]
strategies = list(results.keys())

performance_metrics = ["wall_time", "cpu_time", "throughput"]
efficiency_metrics = ["gil_eff", "speedup", "efficiency"]

workers = 4
num_tasks = 4

# metric direction
METRIC_DIRECTION = {
    "wall_time": "lower is better",
    "cpu_time": "lower is better",
    "throughput": "higher is better",
    "gil_eff": "higher is better",
    "speedup": "higher is better",
    "efficiency": "higher is better",
}

# units
METRIC_UNITS = {
    "wall_time": "s",
    "cpu_time": "s",
    "throughput": "ops/s",
    "gil_eff": "",
    "speedup": "x",
    "efficiency": "",
}


# -------------------------
# Helpers
# -------------------------

def format_time(v):
    """Auto switch to ms if small"""
    if v < 0.1:
        return v * 1000, "ms"
    return v, "s"


# -------------------------
# Plot
# -------------------------

def plot_group(workload, metrics, suffix):
    rows = len(levels)
    cols = len(metrics)

    fig, axes = plt.subplots(rows, cols, figsize=(5 * cols, 3.5 * rows))

    for i, level in enumerate(levels):
        for j, metric in enumerate(metrics):
            ax = axes[i][j] if rows > 1 else axes[j]

            raw_values = [
                results[strat][workload][level][metric]
                for strat in strategies
            ]

            # Handle time unit scaling
            unit = METRIC_UNITS.get(metric, "")
            values = raw_values

            if metric in ["wall_time", "cpu_time"]:
                values, unit = zip(*(format_time(v) for v in raw_values))
                unit = unit[0]

            x = np.arange(len(strategies))

            ax.bar(
                x,
                values,
                color=[STRATEGY_COLORS[s] for s in strategies],
            )

            ax.set_xticks(x)
            ax.set_xticklabels(strategies, rotation=20)

            # Column titles (metric + direction)
            if i == 0:
                direction = METRIC_DIRECTION.get(metric, "")
                ax.set_title(
                    f"{metric.replace('_', ' ').title()}\n({direction})",
                    fontsize=10,
                    pad=12,
                )

            # Row labels (low / med / high)
            if j == 0:
                ax.set_ylabel(f"{level.upper()}\n({unit})")

            ax.grid(axis="y", linestyle="--", alpha=0.3)

    # -------------------------
    # Main Title
    # -------------------------
    fig.suptitle(
        f"{workload.upper()} Workload | workers={workers}, tasks={num_tasks}",
        fontsize=18,
        y=0.98,
    )

    # -------------------------
    # Legend
    # -------------------------
    handles = [
        plt.Rectangle((0, 0), 1, 1, color=STRATEGY_COLORS[s])
        for s in strategies
    ]

    fig.legend(
        handles,
        strategies,
        loc="upper center",
        ncol=len(strategies),
        bbox_to_anchor=(0.5, 0.93),
    )

    # -------------------------
    # Layout
    # -------------------------
    plt.tight_layout(rect=[0, 0, 1, 0.90])

    out_path = os.path.join(plots_dir, f"{workload}_{suffix}.png")
    plt.savefig(out_path, bbox_inches="tight")
    plt.close()

    print(f"Saved {out_path}")


# -------------------------
# Run
# -------------------------

workloads = list(next(iter(results.values())).keys())

for w in workloads:
    plot_group(w, performance_metrics, "performance")
    plot_group(w, efficiency_metrics, "efficiency")