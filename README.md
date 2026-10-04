# AEW 0.2.1 — Artificial Economic World

AEW is a small open-source artificial-life sandbox for studying evolution under artificial economic rules. It is a simulation only: no real money, broker APIs, credentials, network penetration or autonomous access to external systems.

## What v0.2.1 actually implements

- seeded, deterministic simulation runs
- virtual cash, one virtual resource and one virtual market price
- pairwise agent-to-agent resource trading
- resource scarcity, consumption and harvesting
- inheritable/mutating `risk` strategy parameter
- reproduction with parent/generation lineage fields
- bankruptcy/death when virtual cash is exhausted
- JSON snapshots with per-tick history
- PNG dashboard plotting living population and virtual price
- checked-in SVG dashboard wireframe/mockup

This release is intentionally smaller than the longer-term AEW concept. Multiple independent assets, richer strategy code mutation and an interactive real-time web dashboard are not implemented in v0.2.1.

## Requirements

Python 3.10+.

```bash
python -m pip install -r requirements.txt
```

For tests:

```bash
python -m pip install -r requirements-dev.txt
```

## Run a simulation

```bash
python -m aew run --ticks 1000 --agents 100 --seed 42 --out aew_snapshot.json
```

## Generate the dashboard

```bash
python -m aew dashboard aew_snapshot.json --out aew_dashboard.png
```

The checked-in design mockup is `dashboard/mockups/dashboard-wireframe.svg`.

## Tests

```bash
python -m pytest -q
```

The release smoke test used the same public CLI with 50 ticks, 30 agents and seed 42, then generated a PNG dashboard from the resulting JSON snapshot.

## Research idea

A useful shorthand is **Evochora: evolution under artificial physics; AEW: evolution under artificial economics.** AEW asks what strategies and lineages emerge when simulated agents face scarcity, exchange, inheritance, mutation and bankruptcy.

See `docs/EVOCHORA_LETTER.md` for the collaboration outreach draft.

## Safety boundary

AEW is deliberately sandboxed. It does not evade controls, penetrate systems, self-propagate across computers, move real funds or execute real financial trades.

## License

MIT — see `LICENSE`.
