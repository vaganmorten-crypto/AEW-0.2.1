from aew.model import ASSETS, World

def test_model_is_canonical_simulation():
    w=World(10,7); w.run(10); s=w.snapshot()
    assert s["tick"]==10 and set(s["assets"])==set(ASSETS)
