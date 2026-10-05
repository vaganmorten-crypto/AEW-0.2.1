from __future__ import annotations
from dataclasses import asdict, dataclass
from random import Random
from statistics import mean, pstdev
from typing import Any

ASSETS = ("food", "energy", "ore", "data")

@dataclass
class Strategy:
    risk: float
    trade_rate: float
    specialization: int
    mutation_sigma: float = 0.06
    def mutate(self, rng: Random) -> "Strategy":
        clip=lambda x:min(1.0,max(0.0,x))
        spec=self.specialization if rng.random()>=0.12 else rng.randrange(len(ASSETS))
        return Strategy(clip(self.risk+rng.gauss(0,self.mutation_sigma)),clip(self.trade_rate+rng.gauss(0,self.mutation_sigma)),spec,self.mutation_sigma)

@dataclass
class Agent:
    id:int; cash:float; inventory:dict[str,float]; strategy:Strategy
    parent:int|None=None; generation:int=0; age:int=0; alive:bool=True

class World:
    def __init__(self, agents:int=100, seed:int=42):
        if agents<2: raise ValueError("agents must be >= 2")
        self.rng=Random(seed); self.seed=seed; self.tick=0; self.next_id=agents
        self.prices={a:10.0 for a in ASSETS}; self.resources={a:float(agents*18) for a in ASSETS}
        self.population=[Agent(i,100.0,{a:8.0 for a in ASSETS},Strategy(self.rng.uniform(.05,.95),self.rng.uniform(.05,.95),self.rng.randrange(len(ASSETS)))) for i in range(agents)]
        self.history:list[dict[str,Any]]=[]; self._record()
    @property
    def living(self): return [a for a in self.population if a.alive]
    def wealth(self,a): return a.cash+sum(a.inventory[k]*self.prices[k] for k in ASSETS)
    def _trade(self,living):
        self.rng.shuffle(living)
        for a,b in zip(living[::2],living[1::2]):
            if self.rng.random()>(a.strategy.trade_rate+b.strategy.trade_rate)/2: continue
            asset=self.rng.choice(ASSETS); seller,buyer=(a,b) if a.inventory[asset]>b.inventory[asset] else (b,a)
            qty=min(seller.inventory[asset],.2+1.8*buyer.strategy.risk*self.rng.random()); cost=qty*self.prices[asset]
            if qty>0 and buyer.cash>=cost:
                seller.inventory[asset]-=qty; buyer.inventory[asset]+=qty; buyer.cash-=cost; seller.cash+=cost
    def step(self):
        living=self.living
        if not living: self.tick+=1; self._record(); return
        for k in ASSETS: self.resources[k]=min(len(self.population)*25.0,self.resources[k]+max(1.0,len(living)*.08))
        for a in living:
            a.age+=1; asset=ASSETS[a.strategy.specialization]
            extraction=min(self.resources[asset],.15+1.25*(.25+.75*a.strategy.risk)*self.rng.random())
            self.resources[asset]-=extraction; a.inventory[asset]+=extraction
            a.inventory["food"]-=.18; a.inventory["energy"]-=.14; a.cash-=.05
        cap=max(1.0,len(self.population)*25.0)
        for k in ASSETS:
            scarcity=1.0-min(1.0,self.resources[k]/cap)
            self.prices[k]=max(.5,self.prices[k]*(1+self.rng.gauss(0,.008)+.012*(scarcity-.5)))
        self._trade(living); parents=[]
        for a in living:
            if a.cash<=0 or a.inventory["food"]<=0 or a.inventory["energy"]<=0: a.alive=False; continue
            if a.age>25 and self.wealth(a)>520 and self.rng.random()<.025: parents.append(a)
        for p in parents[:max(0,300-len(self.living))]:
            p.cash-=30; inv={k:p.inventory[k]*.18 for k in ASSETS}
            for k in ASSETS: p.inventory[k]*=.82
            self.population.append(Agent(self.next_id,30.0,inv,p.strategy.mutate(self.rng),p.id,p.generation+1)); self.next_id+=1
        self.tick+=1; self._record()
    def run(self,ticks):
        if ticks<0: raise ValueError("ticks must be >= 0")
        for _ in range(ticks): self.step()
    def _record(self):
        living=self.living; risks=[a.strategy.risk for a in living]; gens=[a.generation for a in living]
        self.history.append({"tick":self.tick,"population":len(living),"total_agents_ever":len(self.population),"mean_risk":round(mean(risks),4) if risks else 0.0,"risk_diversity":round(pstdev(risks),4) if len(risks)>1 else 0.0,"max_generation":max(gens,default=0),"prices":{k:round(v,4) for k,v in self.prices.items()},"resources":{k:round(v,4) for k,v in self.resources.items()}})
    def snapshot(self):
        return {"version":"0.3.0.dev0","seed":self.seed,"tick":self.tick,"assets":list(ASSETS),"prices":self.prices,"resources":self.resources,"agents":[asdict(a) for a in self.population],"history":self.history}
