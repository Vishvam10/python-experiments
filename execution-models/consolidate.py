import os
import sys
import json
import platform
import psutil


# -------------------------
# System Info
# -------------------------
def get_system_info():
    return {
        "Operating System": platform.system() + " " + platform.release(),
        "Architecture": platform.machine(),
        "CPU": platform.processor() or "unknown",
        "CPU Cores": psutil.cpu_count(logical=False) or psutil.cpu_count(),
        "Memory": f"{round(psutil.virtual_memory().total / (1024**3), 1)} GB",
        "Python Version": platform.python_version(),
    }


def system_info_to_md(info: dict):
    lines = [
        "## Machine Specs\n",
        "| Property | Value |",
        "|----------|-------|",
    ]
    for k, v in info.items():
        lines.append(f"| {k} | {v} |")
    return "\n".join(lines)


# -------------------------
# Results Formatting
# -------------------------
def format_results(results: dict):
    lines = ["## Benchmark Summary\n"]

    for strat, workloads in results.items():
        lines.append(f"### {strat}\n")

        for w_name, levels in workloads.items():
            lines.append(f"#### {w_name.upper()}\n")

            lines.append(
                "| Level | Wall Time (s) | CPU Time (s) | Throughput | Speedup | Efficiency | GIL Eff | Memory (MB) |"
            )
            lines.append(
                "|-------|---------------|--------------|------------|---------|------------|---------|-------------|"
            )

            for level, vals in levels.items():
                lines.append(
                    f"| {level} | "
                    f"{vals['wall_time']:.4f} | "
                    f"{vals['cpu_time']:.4f} | "
                    f"{vals['throughput']:.2f} | "
                    f"{vals['speedup']:.2f} | "
                    f"{vals['efficiency']:.2f} | "
                    f"{vals['gil_eff']:.2f} | "
                    f"{vals['memory_mb']:.2f} |"
                )

            lines.append("")

    return "\n".join(lines)


# -------------------------
# Plot Embedding
# -------------------------
def embed_plots(plots_dir):
    lines = ["## Plots\n"]

    for file in sorted(os.listdir(plots_dir)):
        if file.endswith(".png"):
            path = os.path.join("plots", file)
            lines.append(f"### {file}")
            lines.append(f"![{file}]({path})\n")

    return "\n".join(lines)


# -------------------------
# Main
# -------------------------
def main(run_dir: str):
    base_path = os.path.join("results", run_dir)
    results_file = os.path.join(base_path, "results.json")
    plots_dir = os.path.join(base_path, "plots")
    output_file = os.path.join(base_path, "report.md")

    if not os.path.exists(results_file):
        raise FileNotFoundError(f"Missing {results_file}")

    with open(results_file, "r") as f:
        results = json.load(f)

    system_info = get_system_info()

    md_parts = [
        f"# Benchmark Report ({run_dir})\n",
        system_info_to_md(system_info),
        "\n---\n",
        embed_plots(plots_dir),
        "\n---\n",
        format_results(results),
    ]

    with open(output_file, "w") as f:
        f.write("\n".join(md_parts))

    print(f"Report generated: {output_file}")


if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python consolidate.py <RUN_DIR>")
        sys.exit(1)

    main(sys.argv[1])
