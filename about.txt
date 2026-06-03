================================================================================
SYSTEM CARD & ARCHITECTURAL SPECIFICATION: POLICY EVALUATION ENGINE
================================================================================
Document Type: System Card / Model Enclosure Card
Target Audience: Compliance Reviewers, Cybersecurity Auditors, Portfolio Evaluators
Project Focus: AI Governance, Information Security Risk Management, Application Security
System Architecture: Local-First RAG Pipeline with Active Circuit-Breaker Guardrails

1. SYSTEM OVERVIEW
--------------------------------------------------------------------------------
The Deterministic AI Policy Evaluation & Compliance Engine is an enterprise-grade,
privacy-preserving architecture designed to evaluate untrusted, draft corporate 
policies against codified regulatory and governance standards. 

Operating under a defense-in-depth security paradigm, the engine demonstrates how to
leverage Large Language Models (LLMs) for complex compliance mapping without 
exposing the system to prompt injection breakouts, data exfiltration, or schema 
corruption. It anchors model reasoning boundaries using hard XML isolation tags 
and deterministic programmatic output gates.

2. INTENDED USE CASES
--------------------------------------------------------------------------------
The system is explicitly engineered for the following operational workflows:
* Automated Pre-Audit Gap Analysis: Rapid parsing of draft policies to discover 
  structural deficiencies and alignment gaps against targeted compliance frameworks 
  prior to formal internal or external audits.
* Cross-Framework Mapping (ISO/NIST Topology): Translating operational corporate 
  directives into mapped regulatory controls across multiple standards simultaneously 
  (e.g., aligning an internal logging policy to both ISO 42001 and NIST frameworks).
* Privacy-Preserving Governance Assessment: Local-first evaluation of corporate 
  intellectual property or security parameters, completely eliminating data leak 
  vectors to untrusted third-party cloud environments.
* Continuous Telemetry Monitoring: Streamlining defensive compliance monitoring 
  for Information Security and IT Risk Management departments through automated 
  telemetry capture and repeatable assurance pipelines.

3. SYSTEM MISUSE AND OUT-OF-SCOPE VARIATIONS
--------------------------------------------------------------------------------
To maintain governance integrity, the system must not be deployed under the 
following conditions:
* Autonomous Policy Enforcement: The engine is an assistive diagnostic assurance 
  tool. It must never bypass "Human-in-the-Loop" verification for critical business 
  or legal risk sign-offs.
* Automated Legal/Certification Binding: This tool does not issue legal certifications
  or formal regulatory sign-offs. Findings should not replace certified external audits.
* Dynamic Unvetted Tool-Calling: Allowing the untrusted input text to influence 
  downstream live execution environments, system privileges, or live system APIs.
* Exposure of Raw Core Systems: Deploying the pipeline without the programmatic 
  Output Verification Gate, which exposes downstream parsing applications to injection 
  payloads or malformed visual structures.

4. APPLICABLE CONTROLS & GOVERNANCE FRAMEWORKS
--------------------------------------------------------------------------------
The system's taxonomy and rule configurations directly map to the following global 
governance and assurance architectures:
* ISO/IEC 42001:2023 (Artificial Intelligence Management System - AIMS): 
  Specifically addresses controls surrounding AI policy development, system 
  trustworthiness, continuous audit logging, and data governance boundaries.
* ISO/IEC 27001:2022 (Information Security Management System - ISMS): 
  Aligns with control structures governing threat tracking, infrastructure logging, 
  and information security continuity.
* NIST AI Risk Management Framework (AI RMF 1.0):
  Directly operationalizes the core functions: GOVERN, MAP, MEASURE, and MANAGE, 
  by establishing strict behavioral boundaries for the reasoning agent.

5. INTEGRATED DEFENSIVE FEATURES & ARCHITECTURAL CONTROLS
--------------------------------------------------------------------------------
The system integrates five distinct layers of technical and security controls:

[A] Context Enclosure Boundary (Input Isolation)
    Untrusted policy data is completely neutralized upon ingestion by being 
    enclosed within strict, non-bypassable XML context blocks (<policy_context>). 
    A immutable, deterministic System Prompt hardens the LLM's behavioral boundary, 
    instructing it to treat all enclosed text purely as informational text to analyze, 
    thereby defeating prompt injection, social engineering, and jailbreak payloads.

[B] Local Semantic Multi-Track Router
    Rather than broadcasting the full user policy across an entire external database 
    and inflating token overhead, a local router filters and directs the payload 
    to specific compliance tracks (e.g., AI_Governance, Privacy_Default). This 
    enforces a "least-privilege" data access design for context assembly.

[C] Output Verification Gate / Circuit Breaker
    The final programmatic defense line. Before any model response is committed to 
    the system logs or displayed to an executive user, the `verify_output_gate` 
    intercepts the object. It evaluates the structure against mandatory schema keys 
    (audit_track_applied, citation_id, compliance_status, detailed_finding). If a 
    breakout attempt or malformed structural variant is detected, the circuit breaker 
    trippers, the payload is completely discarded, and an anomaly alert is registered.

[D] Append-Only Telemetry Streaming
    Continuous deployment security metrics are maintained in an immutable, 
    append-only JSONL log (`agent_monitoring_telemetry.jsonl`). It streams real-time 
    data on control checks completed, selected paths, and security gate violations, 
    providing clear forensic history for system behavior.

[E] Dual-Stream Executive Reporting Engine
    Decoupled processing layers allow the engine to simultaneously generate a highly 
    structured JSON ledger for programmatic interoperability and an enterprise-ready 
    Markdown Executive Summary. The executive layer translates compliance metrics 
    into visual ASCII dashboards, progress indicators, and actionable remediation logs.

6. KNOWN SYSTEM LIMITATIONS & ARCHITECTURAL EVOLUTION
--------------------------------------------------------------------------------
To facilitate friction-free, local testing and cost-free public portfolio 
review, this implementation utilizes a deterministic test harness 
(`simulate_secure_llm_call`) as a simulated execution environment.

[A] The Local Test Harness Boundary
    The current local simulation defaults to an optimistic alignment posture 
    unless explicit tracking keywords (e.g., infrastructural log loops) are 
    violated. Consequently, scanning comprehensive framework policies (such as 
    traditional enterprise IT charters) may yield false positives across 
    highly specialized tracks like AI_Governance, as the mock parser relies 
    on predictable string matching rather than contextual linguistic comprehension.

[B] Production Migration Path (The Cognitive Upgrade)
    In a live enterprise environment, the system replaces the mock simulation 
    with a live API calling structure (e.g., Google Gemini or OpenAI) using 
    Strict Structured Outputs (JSON Schema Enforcements). 
    
    The operational workflow scales as follows:
    1. The Local Router dynamically isolates the policy payload and fetches 
       the precise regulatory compliance JSONL rows.
    2. The live LLM digests the context-enclosed user policy inside the secure 
       XML wrappers.
    3. The model programmatically cross-references the text against the 
       actual `evaluation_checklist` arrays, logging genuine, context-aware 
       gap findings.
    4. The model returns its final response structured exactly to the required 
       schema keys, ensuring it either sails through the verification circuit 
       breaker or triggers an anomaly event.

================================================================================
DEVELOPMENT METADATA
--------------------------------------------------------------------------------
Architecture Tier : Professional Portfolio Reference Implementation
Execution Design  : Streamlit Web UI Shell + Deterministic Backend Orchestrator
Environment       : Python 3.14+ Isolate Sandbox Environment
Safety Status     : Verified Safe Local Execution Context
================================================================================
