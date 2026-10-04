from __future__ import annotations
from dataclasses import dataclass, asdict
from random import Random
from statistics import mean
from typing import Any

@dataclass
class Agent:
    id: int
    cash: float
    resource: float
    risk: float
    parent: int | None = None
    generation: int = 0
    alive: bool = True

class World:
    def __init__(self, agents: int = 100, seed: int = 42):
        if agents < 2:
            raise ValueError("agents must be >= 2")
        self.rng = Random(seed)
        self.seed = seed
        self.tick = 0
        self.next_id = agents
        self.price = 10.0
        self.population = [Agent(i, 100.0, 10.0, self.rng.uniform(0.05, 0.95)) for i in range(agents)]
        self.history: list[dict[str, Any]] = []
        self._record()

    @property
    def living(self):
        return [a for a in self.population if a.alive]

    def step(self) -> None:
        living = self.living
        if len(living) < 2:
            self.tick += 1
            self._record()
            return
        scarcity = max(0.2, 1.0 - len(living) / 1000.0)
        self.price = max(0.5, self.price * (1.0 + self.rng.gauss(0, 0.015) + (1-scarcity)*0.002))
        self.rng.shuffle(living)
        for buyer, seller in zip(living[::2], living[1::2]):
            qty = min(seller.resource, max(0.0, buyer.risk * self.rng.random() * 2.0))
            cost = qty * self.price
            if cost <= buyer.cash:
                buyer.cash -= cost; buyer.resource += qty
                seller.cash += cost; seller.resource -= qty
        for a in living:
            harvest = self.rng.random() * 1.5 * scarcity
            consumption = 0.7 + 0.6 * a.risk
            a.resource += harvest - consumption
            a.cash -= 0.08
            if a.resource < 0:
                a.cash += a.resource * self.price
                a.resource = 0.0
            if a.cash <= 0.0:
                a.alive = False
        parents = [a for a in self.living if a.cash > 180 and a.resource > 12]
        for p in parents[: max(0, 200-len(self.living))]:
            if self.rng.random() < 0.03:
                p.cash -= 40; p.resource -= 3
                child = Agent(self.next_id, 40.0, 3.0, min(1,max(0,p.risk+self.rng.gauss(0,0.05))), p.id, p.generation+1)
                self.next_id += 1; self.population.append(child)
        self.tick += 1
        self._record()

    def run(self, ticks: int) -> None:
        if ticks < 0: raise ValueError("ticks must be >= 0")
        for _ in range(ticks): self.step()

    def _record(self) -> None:
        living = self.living
        self.history.append({"tick": self.tick, "population": len(living), "price": round(self.price,4),
                             "mean_cash": round(mean([a.cash for a in living]),4) if living else 0.0,
                             "mean_risk": round(mean([a.risk for a in living]),4) if living else 0.0})

    def snapshot(self) -> dict[str, Any]:
        return {"version":"0.2.1","seed":self.seed,"tick":self.tick,"price":round(self.price,4),
                "agents":[asdict(a) for a in self.population],"history":self.history}
