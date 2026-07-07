#!/usr/bin/env python3
from __future__ import annotations

import argparse
import json
import re
from datetime import datetime, timezone
from pathlib import Path


CONFIDENCE = {"research": 0.72, "markets": 0.68, "sensor": 0.77, "international": 0.74, "ugc": 0.60}
HIGH_KEYWORDS = {"blackout", "shutdown", "attack", "breach", "explosion", "sanctions", "crackdown", "outage"}
CONTRADICTION_PAIRS = [("blackout", "restored"), ("outage", "restored"), ("degraded", "normal")]


def detect_lang(text: str) -> str:
    return "fa" if re.search(r"[\u0600-\u06FF]", text) else "en"


def normalize_text(text: str) -> str:
    return re.sub(r"\s+", " ", text).strip()


def risk_for(text: str, confidence: float) -> str:
    lowered = text.lower()
    if any(keyword in lowered for keyword in HIGH_KEYWORDS):
        return "high"
    if confidence >= 0.74:
        return "medium"
    if confidence >= 0.64:
        return "medium"
    return "low"


def load_items(path: Path) -> list[dict[str, object]]:
    return json.loads(path.read_text(encoding="utf-8"))


def raw_claims(items: list[dict[str, object]]) -> list[dict[str, object]]:
    now = datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")
    claims = []
    for item in items:
        source_class = str(item.get("source_class", "ugc"))
        text = normalize_text(f"{item.get('title', '')} - {item.get('summary', '')}")
        claims.append(
            {
                "id": item["id"],
                "ts": now,
                "source": item.get("source"),
                "source_class": source_class,
                "lang": detect_lang(text),
                "text": text,
                "link": item.get("link"),
                "confidence": CONFIDENCE.get(source_class, 0.66),
            }
        )
    return claims


def crosscheck(claims: list[dict[str, object]]) -> dict[str, object]:
    contradictions = []
    for left in claims:
        left_text = str(left["text"]).lower()
        for right in claims:
            if left["id"] == right["id"]:
                continue
            right_text = str(right["text"]).lower()
            for a, b in CONTRADICTION_PAIRS:
                if a in left_text and b in right_text:
                    contradictions.append({"left_id": left["id"], "right_id": right["id"], "pattern": f"{a}/{b}"})
    unique = {(c["left_id"], c["right_id"], c["pattern"]): c for c in contradictions}
    return {"claims_reviewed": len(claims), "contradictions": list(unique.values())}


def score_claims(claims: list[dict[str, object]]) -> list[dict[str, object]]:
    scored = []
    for claim in claims:
        enriched = dict(claim)
        enriched["risk"] = risk_for(str(claim["text"]), float(claim["confidence"]))
        scored.append(enriched)
    return scored


def minutes(scored: list[dict[str, object]], report: dict[str, object]) -> str:
    high = [claim for claim in scored if claim["risk"] == "high"]
    lines = [
        "# IntelliClaw Fixture Demo Minutes",
        "",
        f"Claims reviewed: {len(scored)}",
        f"High-risk signals: {len(high)}",
        f"Contradictions flagged: {len(report['contradictions'])}",
        "",
        "## High-Risk Signals",
    ]
    for claim in high:
        lines.append(f"- `{claim['id']}` from {claim['source']}: {claim['text']}")
    lines.extend(["", "## Caveat", "", "Offline fixture demo only; not a live intelligence product.", ""])
    return "\n".join(lines)


def write_json(path: Path, payload: object) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(payload, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


def main() -> None:
    parser = argparse.ArgumentParser(description="Run an offline IntelliClaw fixture demo.")
    parser.add_argument("--fixtures", default="examples/fixtures/rss-items.json")
    parser.add_argument("--out", default="examples/demo-output")
    args = parser.parse_args()

    fixture_path = Path(args.fixtures)
    out_dir = Path(args.out)
    claims = raw_claims(load_items(fixture_path))
    normalized = [dict(claim, normalized_text=claim["text"]) for claim in claims]
    report = crosscheck(normalized)
    scored = score_claims(normalized)

    write_json(out_dir / "raw-claims.json", claims)
    write_json(out_dir / "normalized-claims.json", normalized)
    write_json(out_dir / "crosscheck-report.json", report)
    write_json(out_dir / "scored-claims.json", scored)
    (out_dir / "running-minutes.md").write_text(minutes(scored, report), encoding="utf-8")
    print(f"[fixture-demo] wrote {out_dir}")


if __name__ == "__main__":
    main()
