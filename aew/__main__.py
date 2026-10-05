from __future__ import annotations
import argparse,json
from pathlib import Path
from .simulation import World

def run_cmd(args):
    w=World(args.agents,args.seed); w.run(args.ticks)
    Path(args.out).write_text(json.dumps(w.snapshot(),indent=2),encoding="utf-8")
    print(f"AEW 0.3.0.dev0: tick={w.tick} living={len(w.living)} total={len(w.population)} snapshot={args.out}")

def dashboard_cmd(args):
    import matplotlib.pyplot as plt
    d=json.loads(Path(args.snapshot).read_text(encoding="utf-8")); h=d["history"]; ticks=[x["tick"] for x in h]
    fig,axs=plt.subplots(3,1,figsize=(10,10),sharex=True)
    axs[0].plot(ticks,[x["population"] for x in h]); axs[0].set_ylabel("living agents")
    for asset in d["assets"]: axs[1].plot(ticks,[x["prices"][asset] for x in h],label=asset)
    axs[1].set_ylabel("virtual price"); axs[1].legend(ncol=4)
    axs[2].plot(ticks,[x["risk_diversity"] for x in h],label="risk diversity"); axs[2].plot(ticks,[x["max_generation"] for x in h],label="max generation")
    axs[2].set_xlabel("tick"); axs[2].legend(); fig.suptitle("AEW 0.3.0 — Open-Ended Economic Evolution Laboratory")
    fig.tight_layout(); fig.savefig(args.out,dpi=150); plt.close(fig); print(f"dashboard={args.out}")

def main():
    p=argparse.ArgumentParser(prog="python -m aew",description="AEW closed-world evolutionary economics laboratory"); s=p.add_subparsers(dest="command",required=True)
    r=s.add_parser("run"); r.add_argument("--ticks",type=int,default=1000); r.add_argument("--agents",type=int,default=100); r.add_argument("--seed",type=int,default=42); r.add_argument("--out",default="aew_snapshot.json"); r.set_defaults(func=run_cmd)
    d=s.add_parser("dashboard"); d.add_argument("snapshot"); d.add_argument("--out",default="aew_dashboard.png"); d.set_defaults(func=dashboard_cmd)
    a=p.parse_args(); a.func(a)
if __name__=="__main__": main()
