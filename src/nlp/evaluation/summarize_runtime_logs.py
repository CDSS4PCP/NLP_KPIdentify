import argparse
import csv
import os
import re
from dataclasses import dataclass
from typing import List, Optional


GS42_HEADER = "Evaluating on Gold Standard 42 dataset"
GS91_HEADER = "Evaluating on Gold Standard 91 dataset"
SEQ_SCORE_RE = re.compile(r"Score \(%\)\s*\|\s*([0-9.]+)%\s*\|\s*([0-9.]+)%\s*\|\s*([0-9.]+)%\s*\|\s*([0-9.]+)%")
AVG_EPOCH_RE = re.compile(r"Avg per epoch:\s*([0-9.]+)s")


@dataclass
class RunMetrics:
    log_file: str
    gs42_f1: Optional[float]
    gs91_f1: Optional[float]
    mean_gs_f1: Optional[float]
    avg_epoch_s: Optional[float]
    warning_count: int


def _extract_seqeval_f1(lines: List[str], start_idx: int) -> Optional[float]:
    for idx in range(start_idx, min(start_idx + 300, len(lines))):
        match = SEQ_SCORE_RE.search(lines[idx])
        if match:
            # Columns are precision, recall, f1, accuracy.
            return float(match.group(3))
    return None


def parse_log(path: str) -> RunMetrics:
    with open(path, "r", encoding="utf-8", errors="ignore") as f:
        lines = f.readlines()

    gs42_f1 = None
    gs91_f1 = None
    avg_epoch = None

    for idx, line in enumerate(lines):
        if GS42_HEADER in line:
            gs42_f1 = _extract_seqeval_f1(lines, idx)
        elif GS91_HEADER in line:
            gs91_f1 = _extract_seqeval_f1(lines, idx)

        epoch_match = AVG_EPOCH_RE.search(line)
        if epoch_match:
            avg_epoch = float(epoch_match.group(1))

    warning_count = sum(1 for line in lines if "warning" in line.lower())

    mean = None
    if gs42_f1 is not None and gs91_f1 is not None:
        mean = (gs42_f1 + gs91_f1) / 2.0

    return RunMetrics(
        log_file=os.path.basename(path),
        gs42_f1=gs42_f1,
        gs91_f1=gs91_f1,
        mean_gs_f1=mean,
        avg_epoch_s=avg_epoch,
        warning_count=warning_count,
    )


def rank_runs(rows: List[RunMetrics]) -> List[RunMetrics]:
    def key(row: RunMetrics):
        mean = row.mean_gs_f1 if row.mean_gs_f1 is not None else float("-inf")
        gs91 = row.gs91_f1 if row.gs91_f1 is not None else float("-inf")
        gs42 = row.gs42_f1 if row.gs42_f1 is not None else float("-inf")
        speed = row.avg_epoch_s if row.avg_epoch_s is not None else float("inf")
        return (mean, gs91, gs42, -speed)

    return sorted(rows, key=key, reverse=True)


def write_csv(path: str, rows: List[RunMetrics]) -> None:
    with open(path, "w", newline="", encoding="utf-8") as f:
        writer = csv.writer(f)
        writer.writerow([
            "rank",
            "log_file",
            "gs42_f1",
            "gs91_f1",
            "mean_gs_f1",
            "avg_epoch_s",
            "warning_count",
        ])
        for rank, row in enumerate(rows, start=1):
            writer.writerow([
                rank,
                row.log_file,
                "" if row.gs42_f1 is None else f"{row.gs42_f1:.2f}",
                "" if row.gs91_f1 is None else f"{row.gs91_f1:.2f}",
                "" if row.mean_gs_f1 is None else f"{row.mean_gs_f1:.2f}",
                "" if row.avg_epoch_s is None else f"{row.avg_epoch_s:.2f}",
                row.warning_count,
            ])


def write_summary(path: str, rows: List[RunMetrics], log_dir: str) -> None:
    with open(path, "w", encoding="utf-8") as f:
        f.write("# Runtime Log Research Summary\n\n")
        f.write(f"Log directory: {log_dir}\n\n")
        f.write(f"Parsed logs: {len(rows)}\n\n")

        complete = [r for r in rows if r.mean_gs_f1 is not None]
        incomplete = [r for r in rows if r.mean_gs_f1 is None]
        f.write(f"Complete GS42+GS91 metric logs: {len(complete)}\n")
        f.write(f"Incomplete metric logs: {len(incomplete)}\n\n")

        if rows:
            best = rows[0]
            f.write("## Best Run\n\n")
            f.write(f"- Log: {best.log_file}\n")
            f.write(f"- GS42 F1: {best.gs42_f1 if best.gs42_f1 is not None else 'n/a'}\n")
            f.write(f"- GS91 F1: {best.gs91_f1 if best.gs91_f1 is not None else 'n/a'}\n")
            f.write(f"- Mean GS F1: {best.mean_gs_f1 if best.mean_gs_f1 is not None else 'n/a'}\n")
            f.write(f"- Avg Epoch Time (s): {best.avg_epoch_s if best.avg_epoch_s is not None else 'n/a'}\n")
            f.write(f"- Warning Count: {best.warning_count}\n\n")

        f.write("## Top 5 Runs\n\n")
        for idx, row in enumerate(rows[:5], start=1):
            f.write(
                f"{idx}. {row.log_file} | GS42={row.gs42_f1 if row.gs42_f1 is not None else 'n/a'} "
                f"| GS91={row.gs91_f1 if row.gs91_f1 is not None else 'n/a'} "
                f"| Mean={row.mean_gs_f1 if row.mean_gs_f1 is not None else 'n/a'} "
                f"| Epoch(s)={row.avg_epoch_s if row.avg_epoch_s is not None else 'n/a'} "
                f"| Warnings={row.warning_count}\n"
            )

        if incomplete:
            f.write("\n## Incomplete Logs\n\n")
            for row in incomplete:
                f.write(f"- {row.log_file}\n")


def main() -> None:
    parser = argparse.ArgumentParser(description="Summarize runtime logs for GS metrics and ranking.")
    parser.add_argument(
        "--logDir",
        type=str,
        default="/home/rohangoli/remote_mount/outputs/results/rtx2000_blackwell/2026/05/31",
        help="Directory containing runtime .txt logs",
    )
    parser.add_argument(
        "--csvOut",
        type=str,
        default="runtime_metrics_ranked.csv",
        help="Output CSV filename (relative to logDir if not absolute)",
    )
    parser.add_argument(
        "--summaryOut",
        type=str,
        default="runtime_research_summary.md",
        help="Output summary markdown filename (relative to logDir if not absolute)",
    )
    args = parser.parse_args()

    log_dir = os.path.abspath(args.logDir)
    if not os.path.isdir(log_dir):
        raise FileNotFoundError(f"Log directory not found: {log_dir}")

    logs = [
        os.path.join(log_dir, name)
        for name in sorted(os.listdir(log_dir))
        if name.endswith(".txt")
    ]

    rows = [parse_log(path) for path in logs]
    ranked = rank_runs(rows)

    csv_out = args.csvOut
    if not os.path.isabs(csv_out):
        csv_out = os.path.join(log_dir, csv_out)

    summary_out = args.summaryOut
    if not os.path.isabs(summary_out):
        summary_out = os.path.join(log_dir, summary_out)

    write_csv(csv_out, ranked)
    write_summary(summary_out, ranked, log_dir)

    print(f"Parsed logs: {len(logs)}")
    print(f"Ranked CSV: {csv_out}")
    print(f"Research summary: {summary_out}")


if __name__ == "__main__":
    main()
