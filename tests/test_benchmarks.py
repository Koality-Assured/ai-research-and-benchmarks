"""Unit tests for benchmark suite runner and cost calculator."""

import json
import unittest
from pathlib import Path
import sys

_ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(_ROOT))

from harnesses.runner import load_suite, run_benchmark
from telemetry.cost_calculator import calculate_cost, compare_headroom_savings


class TestResearchAndBenchmarks(unittest.TestCase):
    def setUp(self):
        self.root = _ROOT
        self.suite_file = self.root / "benchmarks" / "suites" / "coding_agent_benchmark_v1.json"

    def test_benchmark_suite_file_loads(self):
        self.assertTrue(self.suite_file.exists())
        data = load_suite(self.suite_file)
        self.assertEqual(data["suite_name"], "coding_agent_benchmark_v1")
        self.assertGreaterEqual(len(data["tasks"]), 3)

    def test_benchmark_dry_run(self):
        data = load_suite(self.suite_file)
        summary = run_benchmark(data, dry_run=True, max_tasks=2)
        self.assertEqual(summary["total_tasks"], 2)
        self.assertEqual(summary["successful_tasks"], 2)
        self.assertEqual(len(summary["results"]), 2)

    def test_cost_calculation(self):
        res = calculate_cost("gpt-4o", input_tokens=1_000_000, output_tokens=1_000_000)
        self.assertAlmostEqual(res["input_cost_usd"], 2.50, places=2)
        self.assertAlmostEqual(res["output_cost_usd"], 10.00, places=2)
        self.assertAlmostEqual(res["total_cost_usd"], 12.50, places=2)

    def test_headroom_savings(self):
        res = compare_headroom_savings(raw_tokens=100_000, compressed_tokens=20_000, model="gpt-4o")
        self.assertEqual(res["compression_percentage"], 80.0)
        self.assertGreater(res["savings_usd"], 0.0)


if __name__ == "__main__":
    unittest.main()
