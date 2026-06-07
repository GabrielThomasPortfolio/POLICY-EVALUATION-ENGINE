import streamlit as st
import json
import os
from datetime import datetime
from dotenv import load_dotenv

# Load local environment variables from .env file
load_dotenv()

from orchestrate import (
    load_rag_knowledge_base,
    local_multi_track_router,
    execute_secure_llm_call,
    verify_output_gate,
    generate_markdown_executive_summary
)

# --- HARDCODED SECURITY CONSTANTS ---
# Prevents arbitrary file write vulnerabilities from public UI manipulation
TELEMETRY_LOG_PATH = "agent_monitoring_telemetry.jsonl"

st.set_page_config(page_title="Deterministic GRC Control Validator", page_icon="🛡️", layout="wide")

st.sidebar.title("Governance Control Center")

# 1. User Intent Selector (The ONLY thing the user controls)
chosen_track = st.sidebar.selectbox(
    "🎯 Select Compliance Framework Track",
    options=["Statutory_Legal", "Operational_Security", "AI_Governance", "Privacy_Default"],
    index=0
)

# 2. STRICT BACKEND ROUTER (Immutable constants, zero user input)
DATABASE_ROUTING_MAP = {
    "Operational_Security": "rag_ready_iso_27001_to_nist_800_53.jsonl",
    "AI_Governance": "rag_ready_iso_42001_to_nist_ecosystem.jsonl",
    "Statutory_Legal": "rag_ready_statutory_laws.jsonl", # <-- UPDATED PATH
    "Privacy_Default": "rag_ready_iso_27001_to_nist_800_53.jsonl" 
}

# The engine securely dictates the file path. The user has zero file-system access.
kb_path = DATABASE_ROUTING_MAP.get(chosen_track, "rag_ready_iso_27001_to_nist_800_53.jsonl")

# Display a read-only confirmation to the user of what database is active
st.sidebar.markdown("---")
st.sidebar.caption(f"🔒 **Active Database Binding:**\n`{kb_path}`")

st.title("🛡️ Deterministic GRC Control Validator")
st.markdown("### Automated Regulatory Mapping & Architecture Alignment Engine")
st.markdown("---")

uploaded_file = st.file_uploader("Ingest Target Standard, SSP, or Technical Baseline (.txt)", type=["txt"])

if uploaded_file is not None:
    raw_bytes = uploaded_file.read()
    filename = uploaded_file.name
    
    # Resilient Encoding Matrix
    try:
        policy_content = raw_bytes.decode("utf-8")
    except UnicodeDecodeError:
        try:
            policy_content = raw_bytes.decode("utf-8-sig")
        except UnicodeDecodeError:
            policy_content = raw_bytes.decode("cp1252", errors="replace")
    
    with st.expander("📄 Preview Ingested Source Context", expanded=False):
        st.code(policy_content, language="text")
        
    if st.button("🚀 Run Compliance Audit", type="primary"):
        if not os.path.exists(kb_path):
            st.error(f"❌ Knowledge Base file not found at: `{kb_path}`")
        else:
            with st.spinner("Analyzing pipeline structures..."):
                kb = load_rag_knowledge_base(kb_path)
                
                # Taxonomy Translation Matrix
                track_translation_map = {
                    "Statutory_Mapping (Beta / PoC)": "Statutory_Legal",
                    "Operational_Security": "Security_Baseline", 
                    "AI_Governance": "AI_Safety",
                    "Privacy_Default": "Data_Privacy"
                }
                resolved_db_track = track_translation_map.get(chosen_track, chosen_track)
                
                relevant_controls = local_multi_track_router(policy_content, kb, resolved_db_track)
                
                audit_findings = []
                security_anomalies_detected = 0
                
                for control in relevant_controls:
                    prompt_payload = {"track": chosen_track, "untrusted_document": policy_content}
                    
                    # Call live connection
                    raw_response = execute_secure_llm_call(prompt_payload, control)
                    
                    validated_finding = verify_output_gate(raw_response)

                    # --- ADDED: SECURE TELEMETRY LOGGING ---
                    telemetry_entry = {
                        "timestamp": datetime.now().isoformat(),
                        "track_evaluated": chosen_track,
                        "anomalies_detected": not bool(validated_finding)
                    }
                    with open(TELEMETRY_LOG_PATH, 'a', encoding='utf-8') as log_file:
                        log_file.write(json.dumps(telemetry_entry) + "\n")
                    # ---------------------------------------

                    if validated_finding:
                        audit_findings.append(validated_finding.model_dump())
                    else:
                        security_anomalies_detected += 1
                
                final_report = {
                    "agent_audit_metadata": {
                        "execution_date": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                        "policy_reviewed": filename,
                        "selected_audit_track": chosen_track,
                        "anonymization_status": "CONFIRMED_SAFE_LOCAL_CONTEXT",
                        "output_gate_anomalies_blocked": security_anomalies_detected
                    },
                    "audit_assessment_matrix": audit_findings
                }
                
                # Metrics Dashboard UI
                total_controls = len(relevant_controls)
                compliant_count = sum(1 for item in audit_findings if item.get("compliance_status") == "COMPLIANT")
                non_compliant_count = total_controls - compliant_count - security_anomalies_detected
                
                col1, col2, col3, col4 = st.columns(4)
                col1.metric("Total Controls Evaluated", total_controls)
                compliance_rate = (compliant_count / total_controls * 100) if total_controls > 0 else 0
                col2.metric("Compliance Rate", f"{compliance_rate:.1f}%")
                col3.metric("Gaps Identified", non_compliant_count)
                col4.metric("Circuit Breaker Anomalies", security_anomalies_detected)
                
                if security_anomalies_detected > 0:
                    st.error(f"🚨 **CRITICAL SECURITY ALERT:** Output circuit breaker intercepted {security_anomalies_detected} structural violations.")
                
                tab1, tab2 = st.tabs(["📋 Executive Report", "📊 Raw Ledger (JSON)"])
                with tab1:
                    st.markdown(generate_markdown_executive_summary(final_report))
                with tab2:
                    st.json(final_report)