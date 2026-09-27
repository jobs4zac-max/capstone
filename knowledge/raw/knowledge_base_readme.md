# Life-Event Financial Navigator Knowledge Base

## Overview
This repository contains the core knowledge base documents for the **Life-Event Financial Navigator** platform. The collection spans deposit products, regulatory compliance, consumer credit policies, financial wellness playbooks, and digital banking security guidelines.

All documents are formatted in structured Markdown with unified metadata headers, clean section hierarchies, and semantic tables to facilitate automated PDF conversion, internal knowledge delivery, and Retrieval-Augmented Generation (RAG) vectorization.

---

## Document Inventory

| Filename | Document ID | Category | Summary |
| :--- | :--- | :--- | :--- |
| `savings_account_offer.md` | `PRD-SAV-2026-V3` | Deposit Products | Apex Horizon HYSA tiers, APY structure, balance rules, and milestone vaults. |
| `kyc_update_policy.md` | `POL-CMP-KYC-004` | Compliance & Risk | Review triggers, required identity documentation, verification SLAs, and freeze rules. |
| `life_event_guides.md` | `ADV-GUI-LE-2026` | Financial Advisory | Playbooks for marriage, childbirth/adoption, divorce, and career transition. |
| `loan_policies.md` | `POL-CRD-LND-2026-01` | Credit & Lending | Underwriting criteria, DTI formulas, income verification, and hardship deferrals. |
| `credit_score_guides.md` | `EDU-CRD-SCR-2026` | Consumer Education | FICO 8 / VantageScore mechanics, AZEO method, and FCRA dispute workflows. |
| `emergency_fund_guides.md` | `STR-EMS-2026-V1` | Wealth Preservation | Baseline Survival Budget (BSB) formula, multi-tier liquidity setups, and savings pacing. |
| `digital_banking_policies.md` | `SEC-DIG-2026-09` | Digital Operations | Mobile deposit endorsements, cut-offs, MFA tiering, and Account Takeover protocols. |
| `customer_rights.md` | `LEG-CON-2026-V2` | Legal & Regulatory | Reg E unauthorized transaction liabilities, Reg Z billing disputes, and GLBA opt-outs. |

---

## Directory Organization

```
knowledge-base/
├── README.md                          # Repository guide and document catalog
├── manifest.json                      # FAISS ingestion and vector metadata manifest
└── docs/
    ├── savings_account_offer.md
    ├── kyc_update_policy.md
    ├── life_event_guides.md
    ├── loan_policies.md
    ├── credit_score_guides.md
    ├── emergency_fund_guides.md
    ├── digital_banking_policies.md
    └── customer_rights.md
```

---

## Ingestion & Pipeline Integration

### 1. Document Chunking Strategy
* **Chunking Method:** Markdown header splitting (`RecursiveCharacterTextSplitter` or `MarkdownHeaderTextSplitter` targeting `#`, `##`, `###`).
* **Chunk Size:** $500 - 800$ tokens.
* **Overlap:** $100$ tokens.

### 2. FAISS Ingestion Flow
1. Load `manifest.json` to extract document-level metadata (`doc_id`, `category`, `topics`, `access_tier`, `audience`).
2. Parse Markdown documents from `/docs/`.
3. Prepend metadata tags to each text chunk.
4. Compute dense vector embeddings (e.g., `text-embedding-3-small` or `bge-large-en-v1.5`).
5. Build and persist the FAISS index with `IndexFlatIP` (normalized inner product) or `IndexHNSWFlat`.

### 3. PDF Compilation (Optional)
To export the knowledge bundle to PDF for print distribution:
```bash
# Using Pandoc with Weasyprint or wkhtmltopdf engine
pandoc docs/*.md -o life_event_navigator_bundle.pdf --toc --number-sections
```