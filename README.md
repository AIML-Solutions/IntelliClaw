# IntelliClaw

> Real-time multi-topic signals pipeline for research, OSINT, job-market monitoring, market-close analysis, and configurable event intelligence.

Built on [OpenClaw](https://github.com/AIML-Solutions) · Operated by [AIML Solutions](https://www.aiml-solutions.com)

---

## What It Does

IntelliClaw is an autonomous intelligence pipeline for monitoring configurable topics and event domains. It can be adapted for arXiv/research feeds, job-search signals, geopolitics, markets, infrastructure, incident response, and historical timelines. It normalizes multilingual content, cross-checks claims for contradictions, scores signals by risk level, and dispatches structured intelligence updates to a live ledger.

In the MultiClaw OS architecture, IntelliClaw is the intelligence layer: public-source signal collection and triage that can feed agent workflows, research briefs, hiring pipelines, market context, or client-defined watchlists.

## Who This Is For

- Analysts and engineers who need configurable research monitoring without a heavyweight platform
- Recruiters or clients evaluating Python/bash automation, source hygiene, and signal-triage design
- Teams building public/private intelligence workflows where credentials, client notes, and sensitive claims must stay separated

## Portfolio Proof

| Area | Evidence |
| --- | --- |
| Source configuration | RSS source list and source-class model |
| Pipeline orchestration | shell orchestrator across harvesting, normalization, cross-checking, scoring, and dispatch |
| Public/private boundary | README and docs require sanitized examples only |
| Example artifacts | `examples/signal-cycle.input.json`, `examples/signal-cycle.output.example.json` |
| Next proof target | fixture-based complete run with tests |

## Example Lanes

- arXiv and technical paper monitoring
- job-search and target-company intelligence
- market close summaries and macro/derivatives signal collection
- OSINT and incident monitoring
- infrastructure and internet availability signals
- custom client or research-topic watchlists

Public examples should stay sanitized. Credentials, private job-search notes, client details, and account-specific market data do not belong in this repository.

## Commercial Use Cases

- Research monitoring for markets, technical papers, jobs, incidents, or client-defined watchlists
- Sanitized intelligence summaries with source and confidence metadata
- Job-search and target-company monitoring as a private workflow
- OSINT-style source normalization and contradiction triage with explicit caveats

## Implementation Status

| Component | Status | Notes |
| --- | --- | --- |
| Feed harvesting | Active | RSS harvesting and source configuration are implemented under `skills/intelliclaw-feed-harvester/` and `operations/IntelliClaw/config/` |
| Normalization | Active | Language/entity normalization skill structure is present |
| Cross-checking | Scaffold | Current contradiction checks are structured but should be expanded with entity/time/source comparison logic |
| Risk scoring | Active/scaffold | Keyword and confidence scoring exists; calibration and evaluation examples are next steps |
| Telegraph/minutes output | Active | Dispatch and cycle-summary skills are included |
| Orchestration | Active | A shell orchestrator coordinates the lane sequence for scheduled or manual runs |

IntelliClaw is best presented as a configurable signal-triage and research-monitoring pipeline. The next quality step is adding fixtures, CI, and sample outputs that demonstrate a complete run end-to-end.

## Pipeline Shape

```
RSS Feeds (7 sources)
       │
       ▼
┌─────────────────┐
│  feed-harvester │  pulls & parses RSS → raw-claims.json
└────────┬────────┘
         │
         ▼
┌──────────────────────┐
│  persian-normalizer  │  entity normalization, FA detection
└────────┬─────────────┘
         │
         ▼
┌───────────────────┐
│  claim-crosscheck │  contradiction detection → crosscheck-report.json
└────────┬──────────┘
         │
         ▼
┌──────────────┐
│  risk-scorer │  confidence × keyword boost → scored-claims.json
└──────┬───────┘
       │
       ▼
┌───────────────────┐
│ telegraph-writer  │  dispatches → telegraph-ledger.md
└──────┬────────────┘
       │
       ▼
┌────────────────┐
│ minutes-scribe │  cycle summary → running-minutes.md
└────────────────┘
```

**Cycle time:** 10 minutes (cron) · **Claims per cycle:** configurable · **Sources:** configurable

---

## Sources

| Label | Class | Coverage |
|---|---|---|
| Reuters-World | international | Wire service |
| AP-World | international | Wire service |
| BBC-World | international | Global coverage |
| Al-Jazeera | international | Regional/global analysis |
| Financial-Times-Markets | markets | Markets and macro coverage |
| NetBlocks-Global | sensor | Infrastructure/internet signals |
| Event-Topic-Feed | configurable | User-selected topic stream |

---

## Quick Start

### Requirements

- Python 3.10+
- `jq`
- `bash`
- `curl`

### Install
```bash
git clone https://github.com/AIML-Solutions/intelliclaw.git
cd intelliclaw
```

### Run a single cycle
```bash
bash skills/intelliclaw-orchestrator/scripts/run_intelliclaw_orchestrator.sh .
```

### Run the offline fixture demo

The fixture demo requires no network access and writes deterministic public-safe outputs under `examples/demo-output/`:

```bash
python3 scripts/run_fixture_demo.py
python3 -m unittest discover -s tests
```

It demonstrates raw claim loading, normalization, contradiction flagging, risk scoring, and a minutes artifact using sanitized example inputs.

### Run every 10 minutes (cron)
```bash
crontab -e
```

Add:
```
*/10 * * * * cd /path/to/intelliclaw && bash skills/intelliclaw-orchestrator/scripts/run_intelliclaw_orchestrator.sh . >> operations/IntelliClaw/live/cycle.log 2>&1
```

### Check dependencies
```bash
bash operations/IntelliClaw/scripts/check_dependencies.sh
```

---

## Configuration

Edit `operations/IntelliClaw/config/rss_sources.txt` to add or remove sources:
```
# label|class|url
Reuters-World|international|https://...
```

Supported classes: `international`, `state`, `opposition`, `sensor`, `ugc`

Each class maps to a base confidence score. See `docs/CONFIGURATION.md`.

---

## Output Files

| File | Description |
|---|---|
| `live/raw-claims.json` | Raw harvested claims |
| `live/normalized-claims.json` | Normalized and language-tagged claims |
| `live/crosscheck-report.json` | Contradiction analysis |
| `live/scored-claims.json` | Risk-scored claims |
| `live/intelliclaw-telegraph-ledger.md` | Live intelligence dispatches |
| `live/intelliclaw-running-minutes.md` | Cycle-by-cycle summary log |
| `live/cycle.log` | Cron execution log |

Public-safe example artifacts are available under [`examples/`](examples/).

Committed fixture-demo outputs are available under [`examples/demo-output/`](examples/demo-output/).

---

## Roadmap

- [x] RSS harvest pipeline (7 sources)
- [x] Multilingual normalization
- [x] Claim cross-check
- [x] Risk scoring
- [x] Telegraph ledger dispatch
- [x] 10-min autonomous cron cycle
- [ ] SignalCockpit integration (browser auth)
- [ ] Contradiction persistence across cycles
- [ ] Cross-cycle deduplication
- [ ] One-pager prose summary
- [ ] Optional translation toggle for multilingual streams
- [ ] Web dashboard
- [ ] Public API

---

## Project Structure
```
intelliclaw/
├── skills/
│   ├── intelliclaw-feed-harvester/
│   ├── intelliclaw-persian-normalizer/
│   ├── intelliclaw-claim-crosscheck/
│   ├── intelliclaw-risk-scorer/
│   ├── intelliclaw-telegraph-writer/
│   ├── intelliclaw-minutes-scribe/
│   └── intelliclaw-orchestrator/
├── operations/
│   └── IntelliClaw/
│       ├── config/
│       │   └── rss_sources.txt
│       ├── scripts/
│       │   └── check_dependencies.sh
│       └── live/          ← gitignored outputs
└── docs/
    ├── ARCHITECTURE.md
    ├── PIPELINE.md
    ├── SKILLS.md
    ├── CONFIGURATION.md
    ├── CONTRIBUTING.md
    └── INTELLIGENCE-LAYER.md
```

---

## License

MIT © 2026 [AIML Solutions](https://www.aiml-solutions.com)
