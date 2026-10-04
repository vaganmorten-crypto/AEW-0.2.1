from __future__ import annotations

import argparse
import json
from pathlib import Path
from .model import World


def run(args):
    world = World(seed=args.seed)
    world.initialize(args.agents)
    world.run(args.ticks)
    Path(args.out).write_text(json.dumps(world.snapshot(), indent=2), encoding="utf-8")
    print(f"AEW 0.2.1: tick={world.tick} population={world.snapshot()['population']} -> {args.out}")


def dashboard(args):
    data = json.loads(Path(args.snapshot).read_text(encoding="utf-8"))
    alive = [a for a in data["agents"] if a["alive"]]
    generations = {}
    for a in alive:
        generations[a["generation"]] = generations.get(a["generation"], 0) + 1
    print("AEW 0.2.1 dashboard")
    print(f"tick: {data['tick']}")
    print(f"living population: {data['population']}")
    print(f"agents ever: {data['total_agents_ever']}")
    print("living by generation:", generations)


p = argparse.ArgumentParser(prog="aew")
sub = p.add_subparsers(required=True)
r = sub.add_parser("run")
r.add_argument("--ticks", type=int, default=1000)
r.add_argument("--agents", type=int, default=100)
r.add_argument("--seed", type=int, default=42)
r.add_argument("--out", default="aew_snapshot.json")
r.set_defaults(func=run)
d = sub.add_parser("dashboard")
d.add_argument("snapshot")
d.set_defaults(func=dashboard)
args = p.parse_args()
args.func(args)
