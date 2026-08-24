"""Calculate token costs and context headroom savings across LLM pricing tiers.

tags: [telemetry, cost, pricing, headroom]
"""

from __future__ import annotations

import argparse
import json
import sys
from typing import Any, Dict, List, Optional

# Pricing per million tokens (USD) - standard representative rates
MODEL_PRICING: Dict[str, Dict[str, float]] = {
    "gpt-4o": {
        "input_per_m": 2.50,
        "output_per_m": 10.00,
        "cache_read_per_m": 1.25,
    },
    "claude-3-5-sonnet": {
        "input_per_m": 3.00,
        "output_per_m": 15.00,
        "cache_read_per_m": 0.30,
    },
    "gemini-1.5-pro": {
        "input_per_m": 3.50,
        "output_per_m": 10.50,
        "cache_read_per_m": 0.875,
    },
    "gemini-1.5-flash": {
        "input_per_m": 0.075,
        "output_per_m": 0.30,
        "cache_read_per_m": 0.01875,
    },
}


def calculate_cost(
    model: str,
    input_tokens: int,
    output_tokens: int,
    cache_read_tokens: int = 0
) -> Dict[str, Any]:
    """Calculate USD cost for a given token usage breakdown."""
    if model not in MODEL_PRICING:
        raise ValueError(f"Unknown model '{model}'. Supported models: {list(MODEL_PRICING.keys())}")

    rates = MODEL_PRICING[model]
    input_cost = (input_tokens / 1_000_000.0) * rates["input_per_m"]
    output_cost = (output_tokens / 1_000_000.0) * rates["output_per_m"]
    cache_cost = (cache_read_tokens / 1_000_000.0) * rates["cache_read_per_m"]
    total_cost = input_cost + output_cost + cache_cost

    return {
        "model": model,
        "input_tokens": input_tokens,
        "output_tokens": output_tokens,
        "cache_read_tokens": cache_read_tokens,
        "total_tokens": input_tokens + output_tokens + cache_read_tokens,
        "input_cost_usd": round(input_cost, 6),
        "output_cost_usd": round(output_cost, 6),
        "cache_cost_usd": round(cache_cost, 6),
        "total_cost_usd": round(total_cost, 6),
    }


def compare_headroom_savings(
    raw_tokens: int,
    compressed_tokens: int,
    model: str = "gpt-4o"
) -> Dict[str, Any]:
    """Compare raw vs compressed context cost savings."""
    raw = calculate_cost(model, input_tokens=raw_tokens, output_tokens=1000)
    comp = calculate_cost(model, input_tokens=compressed_tokens, output_tokens=1000)
    savings_usd = round(raw["total_cost_usd"] - comp["total_cost_usd"], 6)
    ratio = round((1.0 - (compressed_tokens / max(raw_tokens, 1))) * 100, 2)

    return {
        "model": model,
        "raw_tokens": raw_tokens,
        "compressed_tokens": compressed_tokens,
        "compression_percentage": ratio,
        "raw_cost_usd": raw["total_cost_usd"],
        "compressed_cost_usd": comp["total_cost_usd"],
        "savings_usd": savings_usd,
    }


def main(argv: List[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--model", default="gpt-4o", choices=list(MODEL_PRICING.keys()))
    parser.add_argument("--input-tokens", type=int, default=10000)
    parser.add_argument("--output-tokens", type=int, default=1000)
    parser.add_argument("--cache-read-tokens", type=int, default=0)
    parser.add_argument("--compare-raw", type=int, help="Compare raw tokens against input-tokens (treated as compressed)")
    parser.add_argument("--json", action="store_true", help="Output results as JSON")
    args = parser.parse_args(argv)

    if args.compare_raw:
        res = compare_headroom_savings(raw_tokens=args.compare_raw, compressed_tokens=args.input_tokens, model=args.model)
        if args.json:
            print(json.dumps(res, indent=2))
        else:
            print(f"Context Headroom Savings Analysis ({args.model}):")
            print(f"  Raw: {res['raw_tokens']} tokens (${res['raw_cost_usd']})")
            print(f"  Compressed: {res['compressed_tokens']} tokens (${res['compressed_cost_usd']})")
            print(f"  Reduction: {res['compression_percentage']}%")
            print(f"  Savings: ${res['savings_usd']}")
        return 0

    cost = calculate_cost(args.model, args.input_tokens, args.output_tokens, args.cache_read_tokens)
    if args.json:
        print(json.dumps(cost, indent=2))
    else:
        print(f"Token Cost Estimate ({args.model}):")
        print(f"  Input: {cost['input_tokens']} (${cost['input_cost_usd']})")
        print(f"  Output: {cost['output_tokens']} (${cost['output_cost_usd']})")
        print(f"  Total: ${cost['total_cost_usd']}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
