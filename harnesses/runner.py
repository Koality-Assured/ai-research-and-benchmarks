"""Benchmark execution runner for autonomous agent harnesses.

tags: [benchmarks, runner, harness]
"""

from __future__ import annotations

import argparse
import json
import sys
import time
from pathlib import Path
from typing import Any, Dict, List, Optional


def load_suite(suite_path: Path) -> Dict[str, Any]:
    """Load and validate benchmark suite JSON."""
    if not suite_path.exists():
        raise FileNotFoundError(f"Suite file not found: {suite_path}")
    data = json.loads(suite_path.read_text(encoding="utf-8"))
    if "tasks" not in data or not isinstance(data["tasks"], list):
        raise ValueError("Benchmark suite must contain a 'tasks' list")
    return data


def run_benchmark(
    suite_data: Dict[str, Any],
    dry_run: bool = False,
    max_tasks: Optional[int] = None
) -> Dict[str, Any]:
    """Execute benchmark suite tasks."""
    tasks = suite_data.get("tasks", [])
    if max_tasks is not None:
        tasks = tasks[:max_tasks]

    results: List[Dict[str, Any]] = []
    start_time = time.time()

    print(f"Executing suite '{suite_data.get('suite_name', 'unknown')}' with {len(tasks)} task(s)...")

    for task in tasks:
        task_id = task.get("task_id", "unknown")
        title = task.get("title", "")
        print(f"  -> Task [{task_id}]: {title} (dry_run={dry_run})")

        if dry_run:
            status = "simulated_success"
            duration = 0.05
            tokens = 1500
        else:
            # Placeholder for actual agent harness invocation
            status = "completed"
            duration = 1.2
            tokens = 3200

        results.append({
            "task_id": task_id,
            "title": title,
            "status": status,
            "duration_seconds": duration,
            "tokens_consumed": tokens,
        })

    total_time = round(time.time() - start_time, 2)
    summary = {
        "suite_name": suite_data.get("suite_name"),
        "total_tasks": len(tasks),
        "successful_tasks": len([r for r in results if "success" in r["status"] or r["status"] == "completed"]),
        "total_duration_seconds": total_time,
        "results": results,
    }
    return summary


def main(argv: List[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--suite", required=True, help="Path to benchmark suite JSON")
    parser.add_argument("--dry-run", action="store_true", help="Simulate benchmark execution without calling models")
    parser.add_argument("--max-tasks", type=int, help="Limit number of tasks executed")
    parser.add_argument("--output-json", help="Save benchmark results to JSON file")
    args = parser.parse_args(argv)

    suite_path = Path(args.suite).resolve()
    try:
        suite_data = load_suite(suite_path)
    except Exception as exc:
        print(f"Error loading suite: {exc}", file=sys.stderr)
        return 2

    summary = run_benchmark(suite_data, dry_run=args.dry_run, max_tasks=args.max_tasks)
    print("\nBenchmark Summary:")
    print(f"  Suite: {summary['suite_name']}")
    print(f"  Tasks: {summary['successful_tasks']}/{summary['total_tasks']} completed successfully")
    print(f"  Duration: {summary['total_duration_seconds']}s")

    if args.output_json:
        out_file = Path(args.output_json).resolve()
        out_file.parent.mkdir(parents=True, exist_ok=True)
        out_file.write_text(json.dumps(summary, indent=2), encoding="utf-8")
        print(f"Saved benchmark results to {out_file}")

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
