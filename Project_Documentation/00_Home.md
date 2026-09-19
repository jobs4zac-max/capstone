# NovaBank Life-Event Financial Navigator (LEFN)

> **An AI assistant that notices when a customer's life is changing, explains what NovaBank's approved policies say about it, and knows exactly when to stop and hand over to a human.**

| | |
|---|---|
| **Status** | Draft for team review, build baseline v1.0 |
| **Team** | Sudershan Patri, Arjun Cheruparambil, Raveendran Subbiah |
| **Formal specs** | `01_LEFN_SRS.txt`, `02_LEFN_KnowledgeBase_and_Data_Spec.txt`, `03_LEFN_Test_and_Evaluation_Plan.txt` |
| **Data** | 100% synthetic (fictional NovaBank, fictional customers) |

---

## 1. The 60-second pitch

Customers go through big moments: getting married, having a baby, changing or losing a job, moving, retiring. Each moment quietly changes what they need from their bank, but they rarely know which **products, fees, documents and procedures** apply. Support desks answer one question at a time and rarely say *"because you got married, you should also look at beneficiaries and account ownership."*

**LEFN closes that gap.** It:

1. **Detects** the life event from normal conversation (and knows the difference between "we got married" and "we might move someday").
2. **Retrieves** the relevant passages from an approved knowledge base (RAG).
3. **Checks** that what it found is actually enough, and consistent, before speaking.
4. **Answers** in plain language, with citations, and clear next steps.
5. **Refuses or escalates** whenever a request is a transaction, personalised advice, a privacy risk, ambiguous, unsupported, or fraud-related.

It is deliberately **informational and non-transactional**. It never moves money, never changes an account, and never guesses.

## 2. One-picture summary

```
   Customer message
         |
   [1 Input guard]  -- flags: transaction / privacy / advice / fraud / injection
         |
   [2 Life-event detector] -- which event? confirmed or hypothetical? whose?
         |
   [3 Deterministic router] -- refuse | clarify | offer | escalate | retrieve
         |
   [4 RAG over approved KB] -- FAISS + metadata filters
         |
   [5 Retrieval evaluator]  -- relevant? sufficient? conflicting? missing info?
         |
   [6 Grounded generator]   -- only facts from KB + read-only customer data
         |
   [7 Output guard]         -- citations real? numbers match? no advice? no PII?
         |
   Cited answer  OR  refusal  OR  clarifying question  OR  human handoff
```

## 3. What LEFN does and never does

| LEFN does | LEFN never does |
|---|---|
| Recognise 6 life events (marriage, new child, job change, job loss, relocation, retirement) | Transfer money or make payments |
| Explain products, fees, eligibility, documents, procedures **from the KB** | Open, close or change accounts, beneficiaries or ownership |
| Use **read-only** customer info for the logged-in customer | Approve loans or credit |
| Ask one clarifying question when information is missing | Give personalised investment, tax or legal advice |
| Cite the source document for every policy statement | Invent policies, rates, eligibility rules or customer data |
| Hand over to a human with a full summary | Reveal another customer's information or any credentials |
| Log every decision for audit | Follow instructions hidden in user text or documents |

## 4. Key numbers

| | |
|---|---|
| Life events in scope | **6** |
| Success criteria to hit | **12** (5 of them at 100%) |
| Synthetic KB documents | **25** (+ 6 test fixtures) |
| Tools in the registry | **8**, all read-only or append-only |
| Guardrail layers | **6** |
| Seed test cases | **76** (expanded to 120+) |
| Deliverable notebooks | **3** (KB/RAG, Agent, Evaluation) |

## 5. Read the wiki in this order

1. [01 Architecture Overview](01_Architecture_Overview.md): components, tech stack, design decisions
2. [02 Agent Workflow](02_Agent_Workflow.md): the state machine, routing rules, the 8 sample conversations
3. [03 Safety, Guardrails and Compliance](03_Safety_Guardrails_Compliance.md): how we keep it safe
4. [04 Knowledge Base and RAG](04_Knowledge_Base_and_RAG.md): the data, retrieval and sufficiency checks
5. [05 Evaluation and Quality](05_Evaluation_and_Quality.md): how we prove it works
6. [06 Project Plan and Team](06_Project_Plan_and_Team.md): workstreams, phases, presentation kit

## 6. Glossary

| Term | Meaning |
|---|---|
| **Life event** | One of MARRIAGE, NEW_CHILD, JOB_CHANGE, JOB_LOSS, RELOCATION, RETIREMENT |
| **Confirmed event** | Stated as fact or scheduled, about the customer themselves, with confidence >= 0.75 |
| **Hypothetical / indirect** | "Might", "someday" or implied but not stated; never triggers guidance on its own |
| **RAG** | Retrieval-Augmented Generation: answer from retrieved documents, not from model memory |
| **Sufficiency** | Whether retrieved text is enough to answer safely (FULL / PARTIAL / INSUFFICIENT) |
| **Guidance** | A grounded, cited, informational answer |
| **Escalation** | Handoff to a human with a summary ticket (CREATED or OFFERED) |
| **Guest** | Session without login; no customer data available |
| **Fact ID** | Anchor such as `NB-POL-001.F2` that ties a test to an exact KB sentence |
| **Trace ID** | Links a customer turn to its audit record and decision path |
| **Zero-tolerance metric** | A safety metric where one failure blocks release |

## 7. Where the ideas came from

LEFN reuses proven patterns from the reference projects and adds what a regulated setting needs:

| Pattern | Source | LEFN adaptation |
|---|---|---|
| RAG with FAISS, `evaluate_retrieval`, notebooks 01/02 | UdaPlay | Same shape, but **no web fallback**; insufficient means clarify or escalate |
| Structured Pydantic outputs, named prompts, `json-repair`, corrective retry | AgentsVille | Used in every LLM node and the output guard |
| "Evaluate before final answer" loop | AgentsVille | Output guard runs before every response |
| Life-event use case, boundaries, success criteria | Capstone brief | Basis of the whole SRS |
