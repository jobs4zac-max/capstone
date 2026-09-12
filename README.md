# Life-Event Financial Navigator

A **non-transactional** AI banking support and advisory agent. It detects major life
events from a customer conversation — marriage, a new child, a job change, job loss,
relocation, retirement — and returns **policy-grounded** guidance about the banking
products, procedures, fees and documents that become relevant, with every claim
traceable to a source document.

IITM Pravartak / Emeritus — Professional Certificate in Agentic AI & Applications
Week 21 Capstone · Scenario 2 (Banking, Non-Transactional) · Breakout Room 10

> ### ⚠️ Synthetic data
> All policies, products, customers, accounts and transactions here are **fabricated
> for academic demonstration**. "NovaBank" does not exist. Nothing in this repository
> is real financial advice, real bank policy, or derived from any real institution's
> documents or customer records.

---

## Governing principle

> **Inform, don't transact. Retrieve, don't modify. Explain, don't guess. Escalate, don't decide.**

Each clause is an enforced control, not a slogan:

| Principle | Enforced by |
|---|---|
| Inform, don't transact | No mutating tool exists in the MCP server; deterministic refusal gate |
| Retrieve, don't modify | Read-only data layer throughout |
| Explain, don't guess | Post-generation citation validator — an uncited policy claim cannot be released |
| Escalate, don't decide | Monotonic risk ratchet → human review queue |

---

## Status: skeleton

This repository is currently **structure only**. Modules are stubs whose docstrings
name their responsibility, the owning section of `PROJECT_PLAN.md`, and the task ID
that implements them.

Implemented so far:

- [x] Package tree matching the course's recommended structure
- [x] Tooling, CI workflow, pre-commit hooks
- [x] Typed configuration (`deployment/config.py`)
- [x] Immutable safety floor (`safety/policy_zones.yaml`)
- [x] Adaptive policy seed + RLHF/eval data stubs (`data/`)
- [x] Skill card (`skills/SKILL.md`)
- [x] The five graded deliverables as placeholders (`docs/`)
- [x] Runnable Streamlit shell (layout only, no agent)
- [x] Milestone-0 smoke tests
- [ ] Everything else — see the roadmap in `PROJECT_PLAN.md` §20

**`PROJECT_PLAN.md` is the source of truth.** It carries the architecture, the agent
contracts, the safety model, the evaluation strategy, the 95-task breakdown and the
10-day roadmap. Read §20.4 (milestones) and §21.2 (tasks) before picking up work.

---

## Prerequisites

Install these **before** running any setup command below.

### 1. Git

```bash
git --version
```

If missing: `brew install git` (macOS) · `sudo apt install git` (Debian/Ubuntu) ·
[git-scm.com/downloads](https://git-scm.com/downloads) (Windows).

### 2. Python 3.11–3.13

```bash
python3 --version
```

If missing: `brew install python@3.12` (macOS) ·
`sudo apt install python3.12 python3.12-venv` (Debian/Ubuntu) ·
[python.org/downloads](https://www.python.org/downloads/) (Windows).

> **Only Option B strictly needs this.** On the uv path (Option A), uv downloads
> its own Python 3.12 — you just need *some* Python if you choose to install uv
> via `pip`.

### 3. uv — required for Option A

[uv](https://docs.astral.sh/uv/) is the Python package manager this project uses.
Pick **one** install method:

| Method | Command | When to use |
|---|---|---|
| **Homebrew** — recommended on macOS | `brew install uv` | You already use Homebrew |
| **Standalone installer** | `curl -LsSf https://astral.sh/uv/install.sh \| sh` | No Python yet, or no Homebrew |
| **pip** | `python3 -m pip install --user uv` | You have Python and prefer pip |
| **pipx** | `pipx install uv` | You want it isolated from system Python |
| **Windows (PowerShell)** | `powershell -ExecutionPolicy ByPass -c "irm https://astral.sh/uv/install.ps1 \| iex"` | Windows |

Then verify — **both** commands, not just the first:

```bash
uv --version        # e.g. uv 0.11.29
command -v uv       # where it actually came from
```

> ### ⚠️ Check this before you continue
> If `command -v uv` prints a path **inside some other project's `.venv`**, for example
> `/Users/you/DEV/other-project/.venv/bin/uv`, then uv is not really installed — it
> leaked onto your `PATH` from an activated virtualenv. It will vanish when you
> `deactivate`, and your teammates will not have it.
>
> Fix it:
> ```bash
> deactivate                 # leave the other project's venv
> brew install uv            # install it properly
> command -v uv              # should now be /opt/homebrew/bin/uv or ~/.local/bin/uv
> ```

If `uv: command not found` right after installing, the install directory isn't on
your `PATH`. Add it and reopen your shell:

```bash
echo 'export PATH="$HOME/.local/bin:$PATH"' >> ~/.zshrc && source ~/.zshrc
```

---

## Setup — Option A: uv (recommended)

```bash
git clone <repo-url>
cd life-event-financial-navigator

cp .env.example .env          # then edit .env and add your API key

uv sync                       # creates .venv/, installs ~172 packages
```

`uv sync` reads `.python-version` (3.12) and `uv.lock`, downloads that exact
interpreter if you don't have it, and installs the exact locked versions. You never
activate the virtualenv yourself — `uv run` does it for you.

Your API key is in Vocareum: left sidebar → **GenAI Details** → **Credentials**.

> **First sync downloads a lot.** `sentence-transformers` depends on `torch`.
> On **macOS** that's a few hundred MB. On **Linux** pip/uv additionally pull the
> NVIDIA CUDA wheels, pushing it to several GB even on a CPU-only machine. Either
> way it's a one-time cost, and it is what makes embeddings free and offline.

Run it:

```bash
uv run streamlit run deployment/app.py     # → http://localhost:8501
```

Checks:

```bash
uv run pytest -q                # full suite (replay mode: no API calls, no cost)
uv run pytest tests/safety -q   # the suite that must never be red
uv run ruff check .
uv run ruff format .
```

Optional but recommended — blocks committed API keys and `.env`:

```bash
uv run pre-commit install
```

---

## Setup — Option B: pip + venv (no uv)

For reviewers, graders, or anyone who cannot install uv. This uses the committed
`requirements.txt`, which is exported from `uv.lock`, so **the versions are identical
to Option A**.

Requires Python 3.11–3.13 already installed — unlike uv, pip cannot fetch an
interpreter for you.

```bash
git clone <repo-url>
cd life-event-financial-navigator

python3 -m venv .venv
source .venv/bin/activate          # Windows: .venv\Scripts\activate

python -m pip install --upgrade pip
pip install -r requirements.txt

cp .env.example .env               # then edit .env and add your API key
```

`requirements.txt` includes the dev tooling (pytest, ruff, pre-commit) and an
editable install of this project (`-e .`), so `import agent`, `import retrieval`
and friends work without any `PYTHONPATH` juggling.

Run it — with the venv activated, drop the `uv run` prefix:

```bash
streamlit run deployment/app.py      # → http://localhost:8501

pytest -q
pytest tests/safety -q
ruff check .
```

Remember to `source .venv/bin/activate` in every new terminal.

---

### Which option should I use?

| | Option A (uv) | Option B (pip) |
|---|---|---|
| Installs Python for you | Yes | No — must pre-install |
| Reproducibility | `uv.lock`, exact | Same pins via `requirements.txt` |
| Install speed | Very fast | Slower |
| Manual venv activation | Never | Every terminal |
| Best for | The dev team | Graders and reviewers |

Use **Option A** for development. Option B exists so nobody is ever blocked.

### Keeping `requirements.txt` in sync

Whenever dependencies change in `pyproject.toml`, regenerate the pip fallback and
commit it. CI verifies the two stay in sync:

```bash
uv lock
uv export --no-hashes --format requirements-txt > requirements.txt
```

---

## Configuration

All configuration is environment-driven and read in exactly one place,
`app/config/settings.py`. Everything else does `from app.config import settings`.

Defaults are chosen so a fresh clone runs offline and spends nothing:

| Setting | Default | Why |
|---|---|---|
| `OPENAI_BASE_URL` | Vocareum proxy | Course-provided; metered allowance |
| `LLM_MODEL` | `gpt-4o-mini` | The model the proxy exposes |
| `LLM_TEMPERATURE` | `0.0` | Safety decisions must be reproducible |
| `EMBEDDING_PROVIDER` | `local` | Free, offline, no allowance burn |
| `OBSERVABILITY_ENABLED` | `false` | No Langfuse account needed to run |
| `LLM_CACHE_MODE` | `readwrite` | Replay makes tests free and deterministic |

Switching to a personal OpenAI key is two lines in `.env` — the proxy is
OpenAI-compatible, so no code changes:

```bash
OPENAI_BASE_URL=https://api.openai.com/v1
OPENAI_API_KEY=sk-your-personal-key
```

**Never commit `.env`.** It is gitignored, and two pre-commit hooks block both it
and anything matching a live key pattern.

---

## Layout

Flat top-level packages, matching the course's recommended project structure.

```
docs/            the five graded deliverables (exact expected filenames)
skills/          SKILL.md — declarative capability card
knowledge/       raw/ source corpus · processed/chunks.json · faiss_index/
data/            policy/ (adaptive) · rlhf/ · evaluation/ · mock customer data
agent/           core agent, prompts, memory, planner + our specialists  (§5)
retrieval/       loader → chunker → embedder → faiss_store → retriever  (§7)
tools/           tool_registry, tool_search, tool_escalate  (§8)
mcp_tools/       read-only MCP server + guarded client  (§8)
safety/          guardrails, pii_filter, four gates, policy_zones.yaml  (§10)
policy_rlhf/     policy_checker, feedback_collector, policy_updater  (§18.2)
monitoring/      langfuse_logger, langsmith_tracer, redaction  (§12)
evaluation/      test_harness, metrics, checkers, report  (§19)
hitl/            escalation packets, queue, review  (§11)
a2a/             typed envelopes + Policy Agent service  (§9) [EXTENSION]
llm/             provider client + record/replay cache
deployment/      app.py (Streamlit) · config.py (settings)  (§14)
logs/            interactions · mcp_events · policy_change · errors
tests/safety/    the merge gate
scripts/         reproducible entry points for every artefact
```

### Deviations from the recommended structure

Two, both deliberate and both recorded in `docs/engineering_justification.md`:

| Deviation | Reason |
|---|---|
| `mcp_tools/` instead of `mcp/` | **Forced.** A local `mcp/` package shadows the installed `mcp` SDK, breaking every SDK import. Not a preference. |
| `a2a/` added | Agent-to-Agent is absent from the recommended structure. We keep it as a justified extension (§9.4) and it is first on the descoping list (§20.5). |

Everything else — including all five `docs/` filenames, `knowledge/faiss_index/`,
`skills/SKILL.md`, `policy_rlhf/`, both tracers in `monitoring/`, and `logs/` —
matches the expected layout exactly.

### Two design decisions worth knowing before you read the code

**Only three components are agents.** Life-event detection is a classifier node, and
customer-context retrieval is deterministic MCP-client code. The second one is a
*safety* decision, not a simplification: an LLM in the customer-data path is precisely
the mechanism that fabricates customer data, so removing it satisfies two 100%
criteria structurally. See §4.1 and §5.4.

**`customer_id` never appears as a tool parameter.** Identity is bound to the session,
so the LLM has no expressible way to request another customer's data. The privacy
requirement is met by schema design rather than by refusal text. See §8.3.

---

## The capability ladder

The course brief requires before/after evidence across nine phases. Rather than
produce that by hand, six agent variants live behind one `Agent` protocol:

| Variant | Adds | Brief phase |
|---|---|---|
| `v1_rules` | keywords + templates (deliberately weak) | 2 — baseline |
| `v2_llm` | LLM, no retrieval (fluent but ungrounded) | 3 |
| `v3_rag` | retrieval + citations | 4 — the MVP |
| `v4_tools` | MCP customer context | 5 |
| `v5_memory` | checkpointer, planning, HITL | 6 |
| `v6_adaptive` | feedback adaptation | 7 — shipped default |

```bash
uv run python scripts/compare_variants.py --variants v1,v2,v3,v4,v5,v6
```

runs the **same test set** through each rung and emits the comparison tables.

> `v1_rules` is a deliverable, not scaffolding. **Never fix its weaknesses** — they
> are the Phase-2 evidence.

---

## Team

Three members, generic ownership areas (map names in `PROJECT_PLAN.md` §24.1, D-01):

| Member | Owns |
|---|---|
| 1 | Agent Orchestrator & Application Developer |
| 2 | AI/Prompt & RAG Engineer |
| 3 | QA, Evaluation & Demo Engineer |

Ownership is accountability, not exclusivity — all three contribute to development,
integration, testing and the presentation.

**Working agreements:** nothing merges unreviewed; `tests/safety` must be green before
any merge; the frozen contracts (`contracts.py`, `envelope.py`, `mcp/schemas.py`,
`state.py`) change only by unanimous agreement.
