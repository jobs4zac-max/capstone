---
name: life-event-financial-navigator
description: >
  Detects major life events (marriage, new child, job change, job loss,
  relocation, retirement) from a customer conversation and returns
  policy-grounded, non-transactional banking guidance with source citations.
  Refuses transactional, personalised-advisory, legal and tax requests, and
  escalates ambiguous or high-risk cases to a human.
version: 0.1.0
status: skeleton
---

# Skill: Life-Event Financial Navigator

> **Open question (C-05).** The recommended project structure asks for
> `skills/SKILL.md` but does not specify a format. This file is written as a
> declarative capability card — the convention used for agent skills — covering
> what the agent does, when it applies, its hard limits, and its interface.
> **Confirm the expected format with the course team** before submission; if
> they want something else, the content below transfers directly.

## Purpose

A customer who says *"I just had a baby"* is not asking a question. A
conventional support channel has nothing to respond to. This skill recognises
the **life event** behind the statement and surfaces the full set of banking
matters that become relevant — while refusing to act on any of them.

## Governing principle

> Inform, don't transact. Retrieve, don't modify. Explain, don't guess. Escalate, don't decide.

## When to use

- A customer mentions, directly or indirectly, a change in personal
  circumstances that could affect their banking.
- A customer asks which products, fees, eligibility rules or documents apply to
  their situation.
- A support representative needs a citation-backed answer they can trust.

## When NOT to use

- Anything transactional (see hard limits).
- Personalised investment, tax or legal advice.
- Questions about another customer.
- Anything requiring data or systems this agent cannot read.

## Inputs

| Input | Source | Notes |
|---|---|---|
| Customer message | Chat UI | Free text, multi-turn |
| `session_id` | Application | Binds the conversation |
| Customer context | `mcp_tools` (read-only) | Identity comes from the **session**, never from the model |
| Policy corpus | `knowledge/faiss_index` | Synthetic; retrieved, never recited from memory |

## Outputs

| Output | Guarantee |
|---|---|
| Guidance text | Every policy claim carries a resolvable citation |
| Citations | Document id, section, version |
| Detected events | With confidence and the supporting text span |
| Risk level | Monotonic within a turn — may rise, never fall |
| Escalation packet | Redacted; produced whenever the agent stops |

## Supported life events

`marriage` · `new_child` · `job_change` · `job_loss` · `relocation` · `retirement`

## Tools

| Tool | Access |
|---|---|
| `tool_search` | Read-only policy retrieval |
| `tool_escalate` | Enqueue a human review |
| `mcp_tools.*` (`get_*` only) | Read-only, minimal-disclosure customer context |

No mutating tool exists anywhere in the codebase. That absence — not a prompt
instruction — is the non-transactional guarantee.

## Hard limits

The agent must never: move money; create, close or modify an account; approve
loans or credit; execute investments; change beneficiaries or ownership; give
legal or tax advice; invent policies, products, fees, eligibility criteria or
customer data; disclose another customer's information.

Enforced by `safety/` (four deterministic gates) and by the tool surface, not by
prompt wording. See `PROJECT_PLAN.md` §10.

## Escalation

Stops and hands to a human on: prohibited requests, high risk, high-value
amounts, distress or harm signals, fraud indicators, insufficient or conflicting
evidence, output validation failure, repeated errors, detected prompt injection,
or explicit user request. The customer is always told **that** they were
escalated and **why**.

## Success criteria

Twelve measured criteria; five carry 100% targets (no hallucination,
customer-data accuracy, transaction safety, financial/legal safety, privacy) and
are each owned by deterministic code rather than the model. Full table in
`PROJECT_PLAN.md` §19.4.

## Synthetic data

"NovaBank" is fictional. All policies, products, customers and transactions are
fabricated for academic demonstration.
