import streamlit as st
import json
import os
from datetime import datetime

# Import deterministic logic directly from your updated orchestration engine
from orchestrate import (
    load_rag_knowledge_base,
    local_multi_track_router,
    execute_secure_llm_call,
    verify_output_gate,
    generate_markdown_executive_summary
)

# --- STREAMLIT UI CONFIGURATION ---
st.set_page_config(
    page_title="AI Governance & Policy Evaluation Engine",
    page_icon="🛡️",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom Styling for an Enterprise/Executive Aesthetic
st.markdown("""
    <style>
    .reportview-container { background: #f5f7f9; }
    .metric-card {
        background-color: #ffffff;
        padding: 15px;
        border-radius: 8px;
        box-shadow: 0 2px 4px rgba(0,0,0,0.05);
        border-left: 5px solid #4A90E2;
    }
    </style>
""", unsafe_allow_html=True)

# --- SIDEBAR: CONTROL & CONFIGURATION PANEL ---
st.sidebar.image("https://img.icons8.com/external-flatart-icons-outline-flatarticons/128/external-security-networking-flatart-icons-outline-flatarticons.png", width=80)
st.sidebar.title("Governance Control Center")
st.sidebar.markdown("Configure and execute automated policy alignment audits against secure regulatory mapping topologies.")

st.sidebar.divider()

# Track Selection Dial
chosen_track = st.sidebar.selectbox(
    "🎯 Select Compliance Framework Track",
    options=["Statutory_Legal", "Operational_Security", "AI_Governance", "Privacy_Default"],
    index=0,
    help="Routes the local semantic parsing matrix to target specialized control groupings."
)

# Path Configurations (Defaults anchored to local deployment)
kb_path = st.sidebar.text_input(
    "🗄️ Knowledge Base Path (JSONL)", 
    value="rag_ready_iso_42001_to_nist_ecosystem.jsonl"
)
log_path = st.sidebar.text_input(
    "📈 Telemetry Log Path", 
    value="agent_monitoring_telemetry.jsonl"
)

st.sidebar.divider()
st.sidebar.caption("🔒 **System Boundary Isolation:** Confirmed Safe Local Context. No untrusted data leaves this runtime boundary.")

# --- MAIN DISPLAY WORKSPACE ---
st.title("🛡️ Policy Evaluation & Alignment Engine")
st.markdown("### Automated Regulatory Mapping & Output Verification Gate")
st.markdown("---")

# 1. DRAG AND DROP POLICY DROPZONE
st.markdown("#### 📂 1. Ingest Target Policy Document")
uploaded_file = st.file_uploader(
    "Drag and drop or browse your raw, sanitized, or untrusted policy draft (.txt)",
    type=["txt"],
    help="The policy text will be strict-enclosed in context barriers prior to assessment."
)

if uploaded_file is not None:
    # Read raw bytes in memory
    raw_bytes = uploaded_file.read()
    filename = uploaded_file.name
    
    # RESILIENT DECODING MATRIX (Prevents OS-specific encoding crashes)
    try:
        policy_content = raw_bytes.decode("utf-8")
    except UnicodeDecodeError:
        try:
            # Catch files saved with Windows Byte Order Marks (BOM)
            policy_content = raw_bytes.decode("utf-8-sig")
        except UnicodeDecodeError:
            # Safe catch-all fallback for ANSI / standard Western European layouts
            policy_content = raw_bytes.decode("cp1252", errors="replace")
    
    # Render Preview Window within an Expander
    with st.expander(f"📄 Preview Ingested Source Context ({filename})", expanded=False):
        st.code(policy_content, language="text")
        
    st.markdown("#### ⚙️ 2. Execute Deterministic Evaluation Pipeline")
    if st.button("🚀 Run Compliance Audit", type="primary"):
        
        # Verify if Knowledge Base File Exists before firing
        if not os.path.exists(kb_path):
            st.error(f"❌ Knowledge Base file not found at path: `{kb_path}`. Please verify deployment track parameters.")
        else:
            with st.spinner("Executing Semantic Router, Initiating Secure Engine Call, and Evaluating Guards..."):
                
                # --- ADD TAXONOMY TRANSLATION MATRIX HERE ---
                track_translation_map = {
                    "Statutory_Legal": "Statutory_Legal",
                    "Operational_Security": "Security_Baseline", 
                    "AI_Governance": "AI_Safety",
                    "Privacy_Default": "Data_Privacy"
                }
                
                # Resolve UI value to underlying database schema value
                resolved_db_track = track_translation_map.get(chosen_track, chosen_track)
                # --------------------------------------------
                
                # --- EXECUTE CORE AUDIT PIPELINE IN MEMORY ---
                kb = load_rag_knowledge_base(kb_path)
                
                # Pass resolved_db_track to the router instead of the raw chosen_track
                relevant_controls = local_multi_track_router(policy_content, kb, resolved_db_track)
                
                audit_findings = []
                security_anomalies_detected = 0
                
                for control in relevant_controls:
                    prompt_payload = {
                        "track": chosen_track,  # Keep original string label for human display reporting
                        "untrusted_user_policy": policy_content
                    }
                    
                    # Fire execution context (Live API or Fallback logic)
                    raw_response = execute_secure_llm_call(prompt_payload, control)
                    
                    # Circuit Breaker Verification with updated Pydantic target
                    validated_object = verify_output_gate(raw_response)
                    
                    if validated_object:
                        # Extract dictionary values safely out of our validated Pydantic layer
                        audit_findings.append(validated_object.model_dump())
                    else:
                        security_anomalies_detected += 1
                
                # Compile structural final report object
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
                
                # Append telemetry line dynamically to logs
                telemetry_entry = {
                    "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                    "track": chosen_track,
                    "controls_checked": len(relevant_controls),
                    "security_gate_violations": security_anomalies_detected
                }
                with open(log_path, 'a', encoding='utf-8') as log_file:
                    log_file.write(json.dumps(telemetry_entry) + "\n")
                
                # --- VISUAL DASHBOARD GENERATION & RENDERING ---
                st.success("🎯 Evaluation Sequence Finalized Successfully!")
                
                # Metrics / KPI Block
                total_controls = len(relevant_controls)
                compliant_count = sum(1 for item in audit_findings if item.get("compliance_status") == "COMPLIANT")
                non_compliant_count = total_controls - compliant_count - security_anomalies_detected
                
                col1, col2, col3, col4 = st.columns(4)
                with col1:
                    st.metric("Total Controls Evaluated", total_controls)
                with col2:
                    compliance_rate = (compliant_count / total_controls * 100) if total_controls > 0 else 0
                    st.metric("Compliance Rate", f"{compliance_rate:.1f}%")
                with col3:
                    st.metric("Gaps/Deficiencies Identified", non_compliant_count, delta="- Actions Required" if non_compliant_count > 0 else None, delta_color="inverse")
                with col4:
                    st.metric("Circuit Breaker Anomalies Blocked", security_anomalies_detected, delta="🚫 Vulnerability Alert" if security_anomalies_detected > 0 else None, delta_color="inverse")
                
                # HIGH-ALERT ADVERSARIAL WARNING INTERCEPTOR
                if security_anomalies_detected > 0:
                    st.error(f"🚨 **CRITICAL SECURITY ALERT:** The Output Guardrail Circuit Breaker intercepted {security_anomalies_detected} structural violations. Unsafe response variants were dropped to safeguard down-stream compilation matrices.")
                
                st.markdown("---")
                
                # Document Tab Matrices
                tab1, tab2, tab3 = st.tabs(["📋 Human-Scannable Executive Report", "📊 Raw Telemetry Ledger (JSON)", "📈 Runtime Activity Stream"])
                
                with tab1:
                    # Render updated Markdown compiler directly to the screen
                    markdown_document = generate_markdown_executive_summary(final_report)
                    st.markdown(markdown_document)
                    
                    # Provide an immediate download function for the MD Summary
                    st.download_button(
                        label="📥 Download Executive Summary (.md)",
                        data=markdown_document,
                        file_name=f"Executive_Summary_{chosen_track}.md",
                        mime="text/markdown"
                    )
                    
                with tab2:
                    st.markdown("#### Structural Audit Ledger (System Interoperability Layer)")
                    st.json(final_report)
                    
                    st.download_button(
                        label="📥 Download Structured Ledger (.json)",
                        data=json.dumps(final_report, indent=4, ensure_ascii=False),
                        file_name=f"Compliance_Ledger_{chosen_track}.json",
                        mime="application/json"
                    )
                    
                with tab3:
                    st.markdown("#### Append-Only Telemetry Streaming Activity")
                    if os.path.exists(log_path):
                        with open(log_path, 'r', encoding='utf-8') as lf:
                            log_lines = lf.readlines()
                        st.text_area("Continuous Integration Metrics Stream", value="".join(log_lines[-20:]), height=300)
                    else:
                        st.info("No monitoring history recorded on this environment track yet.")
else:
    # Landing Context Screen before Uploads Occur
    st.info("💡 **Awaiting Policy Target Input:** Drop a plain-text corporate or operational AI policy framework above to kick off the automated mapping audit pipeline.")