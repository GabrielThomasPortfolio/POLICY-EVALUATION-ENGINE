GRC Control Validator

A lightweight, deterministic engine for evaluating technical standards, SOPs, and system documentation against security and compliance requirements. Built to support real‑world GRC work where inputs are messy, untrusted, and need structured, defensible evaluation.

What This Project Does
* Analyzes technical documentation (SOPs, SSPs, engineering standards, configs)
* Compares content against codified controls
* Produces clear compliance/non‑compliance decisions
* Includes rationale that can be reviewed or audited
* Uses OpenAI in a bounded, deterministic way — no creative interpretation, no hallucinated controls

Why I Built It
* Most AI “policy evaluators” fail because policies are too high‑level and subjective.
* This project focuses on technical artifacts, where requirements are concrete and evaluation can be consistent.

It reflects how GRC engineering actually works:
* structured inputs
* predictable logic
* traceable decisions
* zero‑trust handling of user content

Key Features
* Deterministic evaluation pipeline
* Input sanitization to prevent prompt injection
* Semantic routing to match documentation to relevant controls
* Guardrails to keep outputs grounded and defensible
* Streamlit UI for quick testing and demos

Tech Stack
* Python
* Streamlit
* OpenAI (constrained, evaluation‑only usage)

Live Demo
https://grc-control-validator-gabrielthomas.streamlit.app

What This Project Demonstrates
This repo highlights my focus on:
* GRC engineering
* AI‑assisted control testing
* Deterministic evaluation design
* Practical automation for compliance and audit workflows

It’s part of a broader effort to build tools that make governance work more scalable, consistent, and reliable.* 
