# Fixed-work timing in two independent experiments

The platform comparison and exact owner/incidence comparison use the baseline algorithm with 128 trajectories, one-step observation batches, and 139/512/512 steps per trajectory on D1/D3/D5. They are separate experiments with separate seed sets and host measurement endpoints.

| Case | Platform GPU mean (s) | Owner-lookup mean (s) | Difference |
|---|---:|---:|---:|
| D1 | 0.7302333000 | 0.8168617900 | 11.8631% |
| D3 | 0.3142489000 | 0.3364233600 | 7.0563% |
| D5 | 0.1503578900 | 0.1595295800 | 6.0999% |

The platform experiment uses seeds 2026100601–2026100610. Its checkpoint time is observed after the kernel and state transfer, before any incumbent transfer and verification triggered by that observation. The run then continues to its time budget. The owner/incidence experiment uses seeds 2026092201–2026092210 and records elapsed time after completing the fixed-step loop, including any incumbent verification triggered by the last observation. Preparation, warmup, and final independent certification are outside both measurements.

The archived CUDA source hash is identical in both experiments: `e46da6945964d2223d1c15b4bad083697891ba476b82c175a8408fb1fad62bdc`. The host drivers and timing endpoints differ. Equal step counts with different seeds do not imply identical search trajectories or operation counts.

The records do not decompose the observed difference into seed effects, measurement overhead, or device-state variation. The table above is therefore descriptive, not a causal estimate of any one source of overhead. The reported speed ratios are computed from paired observations within each experiment. In the owner/incidence experiment, final arrays and incumbent sequences match within each evaluated pair.

Sources: `data/diagnostics/platform_comparison_v1/results_compact.jsonl.gz`, `analysis/figures/platform_analysis.json`, `data/owner_lookup/results.jsonl`, and `data/owner_lookup/analysis.json`. No experimental records or numerical results were changed for this clarification.
