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
- `data/diagnostics/`: seven stages; 1146 stage records represent 1137 distinct runs because nine controls are reused. The 420 ablation runs include 126 pilot runs. Compact exports omit large internal states while preserving quality, solution witnesses, traces, parameters, and timings. In `EXPORT_MANIFEST.json`, `export_sha256` is the hash of the compact export in the private archive and `public_sha256` the hash of the file published here, which holds the same records written with standard JSON separators (and, in `platform_comparison_v1`, local paths replaced by relative identifiers).
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

- `benchmark/generated/`: 18 generated instances with m = n = 10,000, 20,000, and 40,000 items in three families (uniform, heavy-tailed, and spatial with long-range reach), each with two budgets. The budgets are chosen where linear relaxations are weak. `hard_manifest.json` lists every generation parameter, the seed, and the SHA-256 of each uncompressed file. Item costs grow linearly with the set size s_i: w_i = round(100 (1/2 + s_i / (2 s̄)) u_i), with u_i uniform in [0.9, 1.1] and at least 1, so that half of the mean cost is fixed and half follows the set size; profits are uniform integers in [100, 200) in the uniform and heavy-tailed families and lognormal workloads in the spatial family. These instances are archived at Zenodo, [doi:10.5281/zenodo.24094323](https://doi.org/10.5281/zenodo.24094323).
- `benchmark/calibration/`: the five instances with m = n = 5,000 that were used to calibrate the budgets against the LP bound.
- `benchmark/edge/edge_manifest.json`: the parameters, statistics, and SHA-256 hashes of the 18 edge-server placement instances built from the [Shanghai Telecom dataset](https://wangshangguang.github.io/telecom_dataset), and the hash of the dataset archive. The dataset may not be redistributed, so the instances are not included; the manuscript describes how they are built from the original files, and the hashes identify them. To rebuild them byte for byte from the twelve half-month workbooks: aggregate the access records by the latitude and longitude strings of each row, skipping rows without coordinates or user identifier and rows whose coordinates are not valid numbers in range; sort the 3,042 base stations by the numeric latitude and then longitude; give each station a profit equal to its number of records; let site i cover every station within great-circle (haversine) distance R of it, itself included, with Earth radius 6371.0088 km; use unit costs with budget k, or density costs w_i = 100 + floor(100 r_i / n), where r_i ranks the sites by the number of stations within 1 km (ties by index), with budget round(k · mean(w)); and write the dense text format of the public BMCP instances, whose SHA-256 `edge_manifest.json` lists: two empty lines, `m=3042  n=3042  knapsack size=C` (two spaces between fields), an empty line, `The weight of 3042 items`, the costs, an empty line, `The profit of 3042 elements`, the profits, an empty line, `Relation matrix`, and one row of 0/1 values per site; values are separated by single spaces, and every line, the last included, ends with LF (ASCII).
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
| `hard_complete.jsonl`, `hard_complete_s4.jsonl`, `hard_complete_s5.jsonl` | GPU-MTS with the complete neighbourhood; generated instances, five seeds (seeds 1 to 3 in the first file), 300 s |
| `hard_restricted_s1.jsonl`, `hard_restricted_s23.jsonl`, `hard_restricted_s4.jsonl`, `hard_restricted_s5.jsonl` | GPU-MTS with the restricted neighbourhood (K = 4); seed 1, seeds 2 and 3, seed 4, and seed 5 |
| `cpu12_hard300.jsonl`, `cpu24_hard300.jsonl`, and their `_s4` and `_s5` files | CPU port with 12 and 24 threads, GPU seeds (seeds 1 to 3, 4, and 5), 300 s |
| `hard_hexaly.jsonl`, `lsbmcp_hard300.jsonl` | Hexaly 15.0 with 24 threads, and LS-BMCP; five seeds, 300 s |
| `hard_lp.jsonl`, `hard_mip.jsonl` | HiGHS 1.15.1 with 24 threads: LP relaxation (interior point, 1,200 s) and MIP (600 s) |
| `anrma_hard.jsonl` | ANRMA executable, 120 s, kept to document its failures: certified selections on 5 of the 18 instances |
| `edge_complete.jsonl`, `edge_restricted.jsonl`, and their `_s4` and `_s5` files | GPU-MTS with both neighbourhoods; edge instances, five seeds (seeds 1 to 3, 4, and 5), 120 s |
| `edge_hexaly.jsonl`, `lsbmcp_edge.jsonl` | Hexaly and LS-BMCP; five seeds, 120 s |
| `edge_highs.jsonl`, `edge_highs_120.jsonl` | HiGHS MIP with 24 threads: 600 s (reference) and 120 s |
| `public_complete.jsonl` and `public_complete_s2.jsonl` to `public_complete_s5.jsonl` | GPU-MTS with the complete neighbourhood; 90 public instances, five seeds, 60 s |
| `anrma_public.jsonl`, `lsbmcp_public.jsonl` | ANRMA and LS-BMCP on one core; five seeds, 60 s |
| `cpu24_public_large.jsonl` and its `_s4` and `_s5` files | CPU port with 24 threads; 30 large public instances, GPU seeds (seeds 1 to 3, 4, and 5), 60 s |
| `platform.jsonl` | GPU against the CPU port with 24 threads at fixed work; 7 instances, both neighbourhoods, three seeds |
| `kernels.jsonl` | shared-memory against global-memory kernel at fixed work; 4 public instances, three seeds |
| `full_kernel_validation_report.json` | complete-neighbourhood gains checked against brute-force enumeration, and GPU/CPU parity |
| `calibration/` | LP bounds and 30 s GPU-MTS runs on the calibration instances; these runs used an earlier build of the complete-neighbourhood kernel (source SHA-256 `4fe857aa…`) |
| `checks/` | 512-step state checks: global-memory against shared-memory kernel (3 public instances, both incoming scans), CPU port against GPU (a public, an edge and a generated instance, both neighbourhoods, 24 threads), and batch invariance (4 public instances); every pair ends in identical states |
| `repeated/` | original records of the 104 runs that were repeated, with a README |

Runs slowed by background load or by the power management of the operating system were repeated, as Section 5.3 of the manuscript describes; the records in this folder are the ones the manuscript uses, and the original records of the repeated runs are in `repeated/`.

ANRMA is the executable published in [Zequn-Wei/SUKP](https://github.com/Zequn-Wei/SUKP); it runs in a Linux container limited to one core, with an unlimited stack, and its only arguments are the seed and the time limit. LS-BMCP is the code of [AloneKami/LS-BMCP](https://github.com/AloneKami/LS-BMCP) at commit 79de31a, compiled with g++ -O3 and run in the same kind of container with the parameters of its documentation (i_max,1 = 10,000, i_max,2 = 500, λ = 0.9); its published output routine is empty, so a routine that prints the best selection was added. Hexaly is version 15.0 (build 20261026). Neither ANRMA nor LS-BMCP is redistributed here. Each record keeps the selection and the value certified from the instance; for ANRMA and LS-BMCP, the value the program itself reported is kept separately.

Before the deposit, every selection in the witnesses and the run records, 2,500 in total, was recertified from the instance files, and the hashes of all instances were checked.

## How to cite

Please cite the generated benchmark through its Zenodo record and the results through this repository:

- J. Garcia, Generated benchmark instances for the budgeted maximum coverage problem (BMCP), Zenodo, 2026, [doi:10.5281/zenodo.24094323](https://doi.org/10.5281/zenodo.24094323).
- J. Garcia, GPU-MTS: results and reproducible evidence for BMCP, GitHub, 2026, https://github.com/rubincus/bmcp-gpu-mts-results.

## License

The contents of this repository are licensed under [CC BY 4.0](https://creativecommons.org/licenses/by/4.0/); see `LICENSE`. Third-party instances, the Shanghai Telecom dataset, and published values of other methods remain under the terms of their sources and are not redistributed.
