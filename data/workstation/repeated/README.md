# Repeated runs

Original records of the 104 runs that background processes or the power management of the operating system
slowed (Windows efficiency mode moved the processes to the efficiency cores). They were recognized by their
throughput (steps per second, or the model-building time of Hexaly) relative to the other seeds of the same
method and instance, and repeated after power throttling was disabled for the solver processes. The manuscript
uses the repeated runs, which are in the parent folder; these records are kept for completeness.

| File | Runs | Content |
|---|---|---|
| `20261110/cpu12_hard300_s4.jsonl` | 18 | CPU port, 12 threads, seed 4, generated instances; 78% of the throughput of seeds 1-3 |
| `20261110/cpu24_hard300_s4.jsonl` | 18 | CPU port, 24 threads, seed 4; 66% of the throughput of seeds 1-3 |
| `20261110/cpu12_hard300_s4_slow_repeat.jsonl` | 3 | first repeat of three CPU-12 seed-4 cells, at 91-95%; at full speed they reach higher values |
| `20261110/cpu24_hard300_s4_slow_repeat.jsonl` | 1 | first repeat of one CPU-24 seed-4 cell, at 81% |
| `20261110/hard_hexaly_s4_throttled.jsonl` | 18 | Hexaly seed 4, generated instances; model build twice as long as for the other seeds |
| `20261110/edge_hexaly_s4_throttled.jsonl` | 18 | Hexaly seed 4, edge instances; same cause |
| `20261117/cpu24_hard300_s5_background.jsonl` | 8 | CPU port, 24 threads, seed 5, with background load; first cell at 62% |
| `20261117/cpu24_hard300_s5_throttled.jsonl` | 2 | CPU port, 24 threads, seed 5, in efficiency mode; 66% and 75% |
| `20261117/hard_restricted_s5_slow.jsonl` | 18 | GPU-MTS-R, seed 5, in efficiency mode; 94% |

Section 5.3 of the manuscript also states the kept runs that are slower than the other seeds of their method.
