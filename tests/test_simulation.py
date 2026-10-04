from aew.simulation import World

def test_seed_is_deterministic():
    a=World(20,7); b=World(20,7); a.run(25); b.run(25)
    assert a.snapshot()==b.snapshot()

def test_tick_and_snapshot_shape():
    w=World(10,1); w.run(5); s=w.snapshot()
    assert s["tick"]==5 and s["version"]=="0.2.1" and len(s["history"])==6

def test_invalid_population():
    try: World(1,1)
    except ValueError: return
    assert False
