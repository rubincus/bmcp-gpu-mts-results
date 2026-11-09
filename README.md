# GPU-MTS: results and reproducible evidence for BMCP

Public repository containing **90 best feasible solutions**, all **900 benchmark runs** (ten per instance), and the data and scripts used to produce the figures and tables in the GPU-MTS study of the budgeted maximum coverage problem (BMCP). Costs are assigned to items, and each covered element contributes its profit once.

Since November 2026 the repository also contains a benchmark of 18 generated instances with up to 40,000 items, the hashes of 18 edge-server placement instances, and the records of the experiments that the revised manuscript runs on one workstation. They are described in [New benchmark and same-workstation experiments](#new-benchmark-and-same-workstation-experiments-november-2026).

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
- `benchmark/`, `data/workstation/`, `solutions/generated/`, and `solutions/edge/`: the November 2026 additions, described in the last section.

The public deposit supports independent verification of the reported solutions and reproduction of the analyses, figures, and tables. It includes the corresponding Python tools; the CUDA and CPU/OpenMP solver implementations are maintained separately. Original sources and provenance are retained for third-party instances and published reference data.

## Correspondence with the manuscript figures

The labels **Base** (Spanish) and **Baseline** (English) denote the configuration identified as `original` or `base` in the experimental records. Archived identifiers and numerical data remain unchanged. Figures contain axes, legends, and data annotations; the manuscript captions describe the comparison conditions. Files in `paper_assets/es` and `paper_assets/en` correspond to the manuscript revision dated September 21, 2026.

The English attainment figure places last-hit annotations below each panel so that they do not cover any curve. The timing protocols of the platform and owner-lookup experiments are compared in [TIMING_PROTOCOLS.md](docs/TIMING_PROTOCOLS.md).

The tables and the throughput figure of the November 2026 revision are not stored here; they are computed from the records described in the next section.

## New benchmark and same-workstation experiments (November 2026)

The revised manuscript adds instances that are larger and harder than the public benchmark, and it runs every method one at a time on one workstation with an NVIDIA GeForce RTX 5080. This section describes the corresponding data files.

### Contents

- `benchmark/generated/`: 18 generated instances with m = n = 10,000, 20,000, and 40,000 items in three families (uniform, heavy-tailed, and spatial with long-range reach), each with two budgets. The budgets are chosen where linear relaxations are weak. `hard_manifest.json` lists every generation parameter, the seed, and the SHA-256 of each uncompressed file.
- `benchmark/calibration/`: the five instances with m = n = 5,000 that were used to calibrate the budgets against the LP bound.
- `benchmark/edge/edge_manifest.json`: the parameters, statistics, and SHA-256 hashes of the 18 edge-server placement instances built from the [Shanghai Telecom dataset](https://wangshangguang.github.io/telecom_dataset), and the hash of the dataset archive. The dataset may not be redistributed, so the instances are not included; the manuscript describes how they are built from the original files, and the hashes identify them.
- `benchmark/SHA256SUMS`: checksums of the files in `benchmark/`; `sha256sum -c benchmark/SHA256SUMS` checks them from the repository root.
- `data/workstation/`: the run records, copied unchanged from the campaign outputs. `EXPORT_MANIFEST.json` gives the source and SHA-256 of each file.
- `solutions/generated/` and `solutions/edge/`: for each instance, one certified solution that attains the best known value used in the manuscript, together with the rule used to select it.

The instances use the sparse format `BMCP-SPARSE 1` and are compressed with xz:
- the first line is `BMCP-SPARSE 1`;
- the second gives m, n, and the budget;
- the third gives the m item costs, and the fourth the n element profits;
- each further line describes one item as `k e_1 ... e_k`, the k 0-based elements it covers.

| Records in `data/workstation/` | Content |
|---|---|
| `hard_complete.jsonl` | GPU-MTS with the complete neighbourhood; generated instances, three seeds, 300 s |
| `hard_restricted_s1.jsonl`, `hard_restricted_s23.jsonl` | GPU-MTS with the restricted neighbourhood (K = 4); seed 1, and seeds 2 and 3 |
| `cpu12_hard300.jsonl`, `cpu24_hard300.jsonl` | CPU port with 12 and 24 threads, GPU seeds, 300 s |
| `hard_hexaly.jsonl`, `lsbmcp_hard300.jsonl` | Hexaly 15.0 with 24 threads, and LS-BMCP; three seeds, 300 s |
| `hard_lp.jsonl`, `hard_mip.jsonl` | HiGHS with 24 threads: LP relaxation (interior point, 1,200 s) and MIP (600 s) |
| `anrma_hard.jsonl` | ANRMA executable, 120 s, kept to document its failures: certified selections on 5 of the 18 instances |
| `edge_complete.jsonl`, `edge_restricted.jsonl` | GPU-MTS with both neighbourhoods; edge instances, three seeds, 120 s |
| `edge_hexaly.jsonl`, `lsbmcp_edge.jsonl` | Hexaly and LS-BMCP; three seeds, 120 s |
| `edge_highs.jsonl`, `edge_highs_120.jsonl` | HiGHS MIP with 24 threads: 600 s (reference) and 120 s |
| `public_complete.jsonl`, `public_complete_s2.jsonl`, `public_complete_s3.jsonl` | GPU-MTS with the complete neighbourhood; 90 public instances, three seeds, 60 s |
| `anrma_public.jsonl`, `lsbmcp_public.jsonl` | ANRMA and LS-BMCP on one core; three seeds, 60 s |
| `cpu24_public_large.jsonl` | CPU port with 24 threads; 30 large public instances, GPU seeds, 60 s |
| `platform.jsonl` | GPU against the CPU port with 24 threads at fixed work; 7 instances, both neighbourhoods, three seeds |
| `kernels.jsonl` | shared-memory against global-memory kernel at fixed work; 4 public instances, three seeds |
| `full_kernel_validation_report.json` | complete-neighbourhood gains checked against brute-force enumeration, and GPU/CPU parity |
| `calibration/` | LP bounds and 30 s GPU-MTS runs on the calibration instances |

ANRMA is the executable published in [Zequn-Wei/SUKP](https://github.com/Zequn-Wei/SUKP). LS-BMCP is the code of [AloneKami/LS-BMCP](https://github.com/AloneKami/LS-BMCP), with a routine added to print the final selection. Neither is redistributed here. Each record keeps the selection and the value certified from the instance; for ANRMA and LS-BMCP, the value the program itself reported is kept separately.

Before the deposit, every selection in the witnesses and the run records, 1,540 in total, was recertified from the instance files, and the hashes of all instances were checked.
