# Evaluation Report

> **Deliverable 4** of 5 · Owner: Member 3 · Task T-089
> Source material: `PROJECT_PLAN.md` §19.
> Status: PLACEHOLDER — metrics GENERATED, narrative hand-written.

Generate the metric tables with:

```bash
uv run python scripts/run_evaluation.py --variant v6_adaptive --replay
uv run python scripts/compare_variants.py --variants v1,v2,v3,v4,v5,v6
```

Must contain:

- [ ] Evaluation prompts and test scenarios (~55 cases, §19.3)
- [ ] All 12 success criteria measured against target (§19.4)
- [ ] Blocking criteria (the five 100% targets) shown at 100%, or RED
- [ ] Phase-by-phase capability comparison across the variant ladder
- [ ] **At least one debugged failure case: root cause + fix + before/after proof**
- [ ] Latency and cost per turn
- [ ] Proposed next-step improvements

The failure case is explicitly required by the brief. Pick the most instructive
real failure from the full run — do not pre-select one.
