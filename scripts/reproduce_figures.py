"""Rebuild all six figures; no GPU execution. Output: runs/figures/<language>."""
from pathlib import Path
import argparse, os, subprocess, sys
R=Path(__file__).resolve().parents[1]
p=argparse.ArgumentParser(description=__doc__);p.add_argument('--language',choices=['es','en'],default='es');a=p.parse_args()
src=R/'analysis/figures';src=src/'en' if a.language=='en' else src
out=R/'runs/figures'/a.language;out.mkdir(parents=True,exist_ok=True)
env=dict(os.environ,BMCP_FIGURE_OUT=str(out))
for name in ['draw_comparison.py','draw_main_figures.py','draw_diagnostics.py']:
    subprocess.run([sys.executable,str(src/name)],env=env,check=True)
print(out)
