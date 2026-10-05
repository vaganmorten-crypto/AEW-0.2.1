# AEW 0.3.0 — Open-Ended Economic Evolution Laboratory

AEW is a safe, closed-world artificial-life laboratory for studying economic evolution. The 0.3 line expands v0.2.1 from one market into a multi-asset ecology while preserving deterministic, reproducible runs.

## v0.3.0 development scope

- four virtual assets: food, energy, ore and data
- endogenous virtual prices and finite resource pools
- agent-to-agent trade across assets
- inheritable strategy genome: risk, trade rate and specialization
- mutation, reproduction, parent IDs and generations
- bankruptcy/death and natural selection
- evolutionary metrics including risk diversity and maximum generation
- JSON experiment snapshots and multi-panel PNG dashboard

The current development version is `0.3.0.dev0`. It must pass tests and the public CLI smoke test before the final `v0.3.0` tag/release is created.

## Run

```bash
python -m pip install -r requirements.txt
python -m aew run --ticks 1000 --agents 100 --seed 42 --out aew_snapshot.json
python -m aew dashboard aew_snapshot.json --out aew_dashboard.png
python -m pytest -q
```

## Safety boundary

AEW is simulation-only. It has no broker APIs, real-money trading, credentials, network penetration, control evasion or autonomous propagation across computers.

## License

MIT — see `LICENSE`.
