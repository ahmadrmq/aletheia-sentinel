# 🛡️ Aletheia Sentinel: Governance Layer for watsonx Orchestrate

### *Autonomous Policy Enforcement & Forensic Audit System*

---

## 🚨 The Problem
As enterprises deploy Agentic AI (like **IBM watsonx Orchestrate**), the risk of "shadow AI" actions increases. Agents need more than just instructions; they need a **Sentinel**—an autonomous guardrail that:
1.  **Intercepts** every user request before execution.
2.  **Scans** for PII, prompt injection, and toxic content.
3.  **Audits** every interaction in an immutable ledger.

## 💡 The Solution: Aletheia Sentinel
Aletheia is a "Sidecar Agent" designed to pair with IBM watsonx Orchestrate. It acts as a governance firewall.

**Core Workflow:**
1.  **User Input** is intercepted by the Sentinel Interface.
2.  **Watson NLU (Natural Language Understanding)** scans the text for policy violations (e.g., "password", "drop table").
3.  **Governance Logic:**
    * ❌ **Violation:** The request is blocked immediately. A "Threat Log" is written to **IBM Cloudant**.
    * ✅ **Clean:** The request is passed to the **watsonx Orchestrate Agent** for execution.

---

## 🏗️ Architecture
This project serves as a local Proof-of-Concept (PoC) for the **IBM Dev Day AI Demystified Hackathon**.

```mermaid
graph TD
    User([User]) -->|Chat Command| UI[Aletheia Interface]
    UI -->|Intercept| NLU[Watson NLU Simulator]
    NLU -->|Scan Intent| Gate{Policy Check}
    Gate -- Violation --> Block[Block Action]
    Block -->|Log Threat| DB[(Cloudant Audit Log)]
    Gate -- Safe --> Agent[watsonx Orchestrate Agent]
    Agent -->|Execute| Action[Business Outcome]
    Agent -->|Log Success| DB
    style UI fill:#0f62fe,stroke:#fff,color:#fff
    style NLU fill:#24a148,stroke:#fff,color:#fff
    style DB fill:#da1e28,stroke:#fff,color:#fff