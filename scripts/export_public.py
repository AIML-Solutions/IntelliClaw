#!/usr/bin/env python3
"""Export a bounded, public-safe snapshot of the latest cycle to public/.

live/ is gitignored and unbounded (append-only ledgers); public/latest.json is
small and stable so the website can render it directly.
"""

from __future__ import annotations

import json
from collections import Counter
from datetime import datetime, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
LIVE = ROOT / "operations" / "IntelliClaw" / "live"
PUBLIC = ROOT / "public"
TOP_N = 12
TEXT_LIMIT = 220


def main() -> int:
    scored_path = LIVE / "scored-claims.json"
    if not scored_path.exists():
        raise SystemExit("no scored claims — run the cycle first")
    scored = json.loads(scored_path.read_text(encoding="utf-8"))
    crosscheck_path = LIVE / "crosscheck-report.json"
    contradictions = 0
    if crosscheck_path.exists():
        contradictions = len(json.loads(crosscheck_path.read_text(encoding="utf-8")).get("contradictions", []))

    risk_counts = Counter(str(c.get("risk", "low")) for c in scored)
    by_source = Counter(str(c.get("source", "unknown")) for c in scored)
    high = [c for c in scored if c.get("risk") == "high"]
    high.sort(key=lambda c: (-float(c.get("confidence", 0)), str(c.get("ts", ""))))

    snapshot = {
        "generated_at": datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ"),
        "cycle": {
            "signals": len(scored),
            "high": risk_counts.get("high", 0),
            "medium": risk_counts.get("medium", 0),
            "low": risk_counts.get("low", 0),
            "contradictions": contradictions,
            "sources": [{"source": s, "count": n} for s, n in by_source.most_common()],
        },
        "top_high": [
            {
                "source": c.get("source"),
                "text": str(c.get("text", ""))[:TEXT_LIMIT],
                "link": c.get("link"),
                "confidence": c.get("confidence"),
                "ts": c.get("ts"),
            }
            for c in high[:TOP_N]
        ],
    }
    PUBLIC.mkdir(exist_ok=True)
    (PUBLIC / "latest.json").write_text(json.dumps(snapshot, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    onepager = LIVE / "intelliclaw-onepager-ledger.md"
    if onepager.exists():
        (PUBLIC / "onepager.md").write_text(onepager.read_text(encoding="utf-8"), encoding="utf-8")
    print(f"[export] {len(scored)} signals, {len(high)} high-risk -> public/latest.json")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
