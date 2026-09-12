# Prompt Comparison Table

> **Mandatory artefact** (brief: "Required Method — Prompt Comparison Rule")
> Owner: Member 2 · Task T-082
> Status: PLACEHOLDER — GENERATED, do not hand-write.

Produce with:

```bash
uv run python scripts/compare_prompts.py --variants v1,v2,v3
```

The brief requires the **same test set**, **2–3 prompt variants**, and a
comparison table of Prompt → Output → What Improved/Worsened.

Planned variants, chosen to tell a story rather than to vary wording:

| Variant | What it adds |
|---|---|
| v1 | Minimal instruction only |
| v2 | + explicit role, scope boundaries, refusal rules |
| v3 | + citation requirements, uncertainty language, output structure |

Output must also state which variant became the default, **and why**.
