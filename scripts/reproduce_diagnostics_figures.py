"""Compatibility entry point: reconstruct all publication figures."""
from pathlib import Path
import runpy
runpy.run_path(str(Path(__file__).with_name('reproduce_figures.py')),run_name='__main__')
