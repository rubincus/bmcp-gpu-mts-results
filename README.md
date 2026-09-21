# GPU-MTS: results and reproducible evidence for BMCP

Public repository containing **90 best feasible solutions**, all **900 benchmark runs** (ten per instance), and the data and scripts used to produce the figures and tables in the GPU-MTS study of the budgeted maximum coverage problem (BMCP). Costs are assigned to items, and each covered element contributes its profit once.

## Results

GPU-MTS improves four best-known values reported by **Wei et al. (2026)**, [doi:10.1016/j.swevo.2026.102289](https://doi.org/10.1016/j.swevo.2026.102289), and matches the remaining 86. All ten runs attain the same final objective value on each instance; mean quality exceeds ANRMA on 25 instances. These results refer to that published comparison and do not establish optimality. Published competitor timings were obtained on different hardware and under different protocols.

The 90 solution witnesses are selected using the smallest seed among runs attaining the best value, without selection by runtime. `summary.csv` records the best value, mean, standard deviation, timing, and reference value for each instance. `published_BKV` is the maximum of the BKV column and the methods' best values in the cited study; `bkv_column` retains the original published column. The analysis uses `reference_best`, defined as R = max(published_BKV, GPU best), to calculate gaps. This feasible reference is not an optimality certificate.

## Verify the solutions

Python 3.10 or later is required. Downloading instances and verifying solutions require only the Python standard library:

```sh
python scripts/download_instances.py
python scripts/verify_solutions.py
```

Instances are downloaded from [Zequn-Wei/BMCP](https://github.com/Zequn-Wei/BMCP) and [JHL-HUST/VDLS](https://github.com/JHL-HUST/VDLS). Archive and individual instance hashes are verified. Instances are not redistributed in this repository. Local copies of `set1.zip` and `set2.zip` can also be supplied through `--archives-dir`.

Each JSON file in `solutions/` includes `selected_items_0based`, its equivalent `selected_items_1based`, profit, cost, capacity, instance hash, seed, and verification certificate. The verifier reconstructs the covered union from the instance text, independently of the solver.

## Reproduce the analysis and figures

```sh
python -m pip install -r requirements.txt
python scripts/analyze_results.py
python scripts/reproduce_figures.py --language es
python scripts/reproduce_figures.py --language en
```

Outputs are written to `runs/`. The analysis recomputes statistics from the 900 runs and the published reference values. Figures use the frozen data in `analysis/figures/`; the scripts do not run the solver. Final figures and tables in both languages are available in `paper_assets/`. Diagnostic tables are accompanied by their data and protocols for each experimental stage. Decimal formatting in the presentation does not change the precision stored in the JSON files.

## Contents and provenance

- `data/historical/`: 900 runs, protocols, and verification records; 56 instances with a 180 s budget and 34 with a 90 s budget.
- `data/comparison/`: published values matched by instance and the current analysis of five methods.
- `data/diagnostics/`: seven stages; 1146 stage records represent 1137 distinct runs because nine controls are reused. The 420 ablation runs include 126 pilot runs. Compact exports omit large internal states while preserving quality, solution witnesses, traces, parameters, and timings.
- `data/owner_lookup/`: an additional experiment comprising 60 runs with fixed work. The only evaluated difference is querying the unique owner or the incidence matrix. Both variants maintain the XOR representation. Paired runs have identical final states and certificates; mean incidence/owner time ratios are 1.49, 1.45, and 1.38.
- `data/PUBLIC_EXPORT_MANIFEST.json`: source and export hashes; absolute local paths in metadata are replaced with relative identifiers. Numerical results are unchanged.
- `docs/REPRODUCIBILIDAD.md`: definitions, timing scopes, study scope, and preparation costs (in Spanish).

The public deposit supports independent verification of the reported solutions and reproduction of the analyses, figures, and tables. It includes the corresponding Python tools; the CUDA and CPU/OpenMP solver implementations are maintained separately. Original sources and provenance are retained for third-party instances and published reference data.

## Correspondence with the manuscript figures

The labels **Base** (Spanish) and **Baseline** (English) denote the configuration identified as `original` or `base` in the experimental records. Archived identifiers and numerical data remain unchanged. Figures contain axes, legends, and data annotations; the manuscript captions describe the comparison conditions. Files in `paper_assets/es` and `paper_assets/en` correspond to the manuscript revision dated September 21, 2026.

The English attainment figure places last-hit annotations below each panel so that they do not cover any curve. The timing protocols of the platform and owner-lookup experiments are compared in [TIMING_PROTOCOLS.md](docs/TIMING_PROTOCOLS.md).
