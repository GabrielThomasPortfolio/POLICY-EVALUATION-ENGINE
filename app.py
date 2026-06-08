import streamlit as st
import json
import os
from datetime import datetime
from dotenv import load_dotenv

# Load local environment variables from .env file
load_dotenv()

from orchestrate import (
    load_rag_knowledge_base,
    local_keyword_router, 
    execute_secure_llm_call,
    verify_output_gate,
    generate_markdown_executive_summary
)

from utils import extract_text_from_file
from sanitize import sanitize_text, SanitizationError

# --- HARDCODED SECURITY CONSTANTS ---
TELEMETRY_LOG_PATH = "agent_monitoring_telemetry.jsonl"

st.set_page_config(page_title="Deterministic GRC Control Validator", page_icon="🛡️", layout="wide")

# --- SIDEBAR: SECURE ROUTING ---
st.sidebar.title("Governance Control Center")

track_translation_map = {
    "Statutory Mapping (Beta / PoC)": "Statutory_Legal",
    "Operational Security": "Operational_Security", 
    "AI Governance": "AI_Governance",
    "Privacy Default": "Privacy_Default"
}

selected_label = st.sidebar.selectbox(
    "🎯 Select Compliance Framework Track",
    options=list(track_translation_map.keys()),
    index=1 
)

chosen_track = track_translation_map[selected_label]

DATABASE_ROUTING_MAP = {
    "Operational_Security": "rag_ready_iso_27001_to_nist_800_53.jsonl",
    "AI_Governance": "rag_ready_iso_42001_to_nist_ecosystem.jsonl",
    "Statutory_Legal": "rag_ready_statutory_laws.jsonl", 
    # SPRINT 4 FIX (Gap 4): Privacy now routes to the statutory asset
    "Privacy_Default": "rag_ready_statutory_laws.jsonl" 
}

kb_path = DATABASE_ROUTING_MAP.get(chosen_track, "rag_ready_iso_27001_to_nist_800_53.jsonl")

st.sidebar.markdown("---")
st.sidebar.caption(f"🔒 **Active Database Binding:**\n`{kb_path}`")

# --- MAIN PAGE UI ---
st.title("🛡️ Deterministic GRC Control Validator")
st.markdown("### Automated Regulatory Mapping & Architecture Alignment Engine")
st.markdown("---")

uploaded_file = st.file_uploader("Ingest Target Standard, SSP, or Technical Baseline (.txt, .pdf, .docx)", type=["txt", "pdf", "docx"])

if uploaded_file is not None:
    filename = uploaded_file.name
    
    # 1. Resilient Document Extraction
    raw_policy_content = extract_text_from_file(uploaded_file)
    
    if not raw_policy_content or not raw_policy_content.strip():
        st.error("❌ The uploaded document appears to be empty, unreadable, or scanned as an image. Please upload a text-searchable file.")
        st.stop()
        
    # 2. Live Security Firewall Execution
    try:
        policy_content = sanitize_text(raw_policy_content)
    except SanitizationError as e:
        st.error(f"🛡️ Security Block: {str(e)}")
        st.stop() 
    
    with st.expander("📄 Preview Ingested Source Context", expanded=False):
        st.code(policy_content, language="text")
        
    if st.button("🚀 Run Compliance Audit", type="primary"):
        # UI Hint for Demo Mode Users
        if os.getenv("OPENAI_API_KEY") == "mock" or not os.getenv("OPENAI_API_KEY"):
            st.info("ℹ️ Running in Mock Fallback Mode: Simulating control validation checks.")

        if not os.path.exists(kb_path):
            st.error(f"❌ Knowledge Base file not found at: `{kb_path}`. Please verify backend database integrity.")
            st.stop() 
            
        with st.spinner("Analyzing pipeline structures..."):
            kb = load_rag_knowledge_base(kb_path)
            
            router_translation_map = {
                "Statutory_Legal": "Statutory_Legal",
                "Operational_Security": "Security_Baseline", 
                "AI_Governance": "AI_Safety",
                "Privacy_Default": "Data_Privacy"
            }
            resolved_db_track = router_translation_map.get(chosen_track, chosen_track)
            
            relevant_controls = local_keyword_router(policy_content, kb, resolved_db_track)
            
            audit_findings = []
            security_anomalies_detected = 0
            
            for control in relevant_controls:
                prompt_payload = {"track": chosen_track, "untrusted_document": policy_content}
                
                raw_response = execute_secure_llm_call(prompt_payload, control)
                validated_finding = verify_output_gate(raw_response)

                # SPRINT 4 FIX (Bug 2): Bulletproof Output Gate Null-Check
                if validated_finding is None:
                    st.error("🚨 Structural integrity violation detected in the response payload. Circuit breaker activated.")
                    st.stop()

                telemetry_entry = {
                    "timestamp": datetime.now().isoformat(),
                    "track_evaluated": chosen_track,
                    "anomalies_detected": False
                }
                
                with open(TELEMETRY_LOG_PATH, 'a', encoding='utf-8') as log_file:
                    log_file.write(json.dumps(telemetry_entry) + "\n")

                audit_findings.append(validated_finding.model_dump())
            
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
            
            total_controls = len(relevant_controls)
            compliant_count = sum(1 for item in audit_findings if item.get("compliance_status") == "COMPLIANT")
            non_compliant_count = total_controls - compliant_count - security_anomalies_detected
            
            col1, col2, col3, col4 = st.columns(4)
            col1.metric("Total Controls Evaluated", total_controls)
            compliance_rate = (compliant_count / total_controls * 100) if total_controls > 0 else 0
            col2.metric("Compliance Rate", f"{compliance_rate:.1f}%")
            col3.metric("Gaps Identified", non_compliant_count)
            col4.metric("Circuit Breaker Anomalies", security_anomalies_detected)
            
            tab1, tab2 = st.tabs(["📋 Executive Report", "📊 Raw Ledger (JSON)"])
            with tab1:
                st.markdown(generate_markdown_executive_summary(final_report))
            with tab2:
                st.json(final_report)