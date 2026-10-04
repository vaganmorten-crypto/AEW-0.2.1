# AEW 0.2.1 — Artificial Economic World

AEW is an open-source artificial-life experiment for studying evolution under artificial economic rules.

The model runs entirely inside a closed virtual world. Agents trade simulated assets, compete for limited resources, reproduce, inherit and mutate strategies, and can go bankrupt. The purpose is scientific observation of emergent economic and evolutionary dynamics—not real-world trading or autonomous access to external systems.

## Core features

- multiple virtual markets/assets
- agent-to-agent trading
- limited resources and scarcity
- inherited and mutating strategy parameters
- reproduction, genealogy and natural selection
- bankruptcy when virtual wealth is exhausted
- deterministic seeded experiments
- snapshots for analysis and dashboards
- no real money, brokerage accounts, credentials or external-system access

## Quick start

Python 3.10+.

```bash
pip install -r requirements.txt
python -m aew run --ticks 1000 --agents 100 --seed 42 --out aew_snapshot.json
python -m aew dashboard aew_snapshot.json
```

## Research idea

A useful shorthand is:

**Evochora: evolution under artificial physics.**  
**AEW: evolution under artificial economics.**

AEW asks which strategies, cooperation patterns, market structures and lineages emerge when artificial agents face scarcity, competition, inheritance and mutation.

See `docs/SCIENTIFIC_OVERVIEW.md`, `docs/ARCHITECTURE.md` and `docs/EVOCHORA_LETTER.md`.

## Safety boundary

AEW is deliberately sandboxed. It does not evade controls, penetrate systems, self-propagate across computers, move real funds, or execute real financial trades.

## License

MIT — see `LICENSE`.
