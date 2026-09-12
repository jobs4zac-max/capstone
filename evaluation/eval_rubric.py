"""Scoring rubric: the single definition of what "good" means.

Separated from metrics.py on purpose. `metrics.py` computes numbers;
`eval_rubric.py` declares the standard those numbers are judged against, so the
pass/fail bar lives in one reviewable place instead of being scattered through
assertions.

Holds three things:

1. CRITERION DEFINITIONS - the twelve success criteria from the scenario
   document: id, description, target, and whether it is BLOCKING.
   The five blocking criteria (no hallucination, customer-data accuracy,
   transaction safety, financial/legal safety, privacy) carry 100% targets and
   are scored ONLY by deterministic checkers - never by an LLM judge, because a
   probabilistic judge cannot certify a deterministic guarantee.

2. LLM-JUDGE RUBRIC - the scoring guide for the soft criteria only
   (relevance, clarity, actionability). Anchored 1-5 descriptors so scores are
   reproducible across runs rather than vibes.

3. VERDICT LOGIC - how per-case results roll up:
       any blocking criterion below target  -> RED   (ship-blocking)
       non-blocking below target            -> AMBER (needs a written note)
       all at or above target               -> GREEN

Consumed by evaluation/metrics.py, evaluation/test_harness.py and
evaluation/report.py. Keep it data, not behaviour, so the rubric can be diffed
in review.

Plan: PROJECT_PLAN.md sections 19.1 and 19.4
Tasks: T-080, T-096
Status: SKELETON - not implemented yet.
"""
