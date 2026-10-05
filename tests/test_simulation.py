from aew.simulation import ASSETS,World

def test_seed_is_deterministic():
    a=World(20,7); b=World(20,7); a.run(25); b.run(25); assert a.snapshot()==b.snapshot()
def test_snapshot_and_assets():
    w=World(10,1); w.run(5); s=w.snapshot(); assert s["tick"]==5 and s["version"]=="0.3.0.dev0" and set(s["assets"])==set(ASSETS) and len(s["history"])==6
def test_lineage_and_strategy_mutation_can_run():
    w=World(30,3); w.run(200); assert all(a.generation>=0 for a in w.population); assert all(0<=a.strategy.risk<=1 for a in w.population)
def test_resources_nonnegative():
    w=World(25,4); w.run(100); assert all(v>=0 for v in w.resources.values())
def test_invalid_population():
    try: World(1,1)
    except ValueError: return
    assert False
