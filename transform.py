import csv
import json
import os

def get_regulatory_overlay(framework_type, iso_id, control_domain):
    """
    Dynamic Legal Overlay Engine.
    Maps high-level legislation parameters to engineering controls automatically.
    """
    mapping = {}
    tracks = ["Security_Baseline"]
    
    clean_id = str(iso_id).strip()
    domain = str(control_domain).upper()

    if framework_type == "ISO_27001":
        # 1. Privacy Overlays (GDPR & CCPA) for Data Handling
        if any(target in clean_id for target in ["5.12", "5.13", "5.14", "5.33", "5.34", "8.10", "8.11", "8.12", "8.33"]):
            mapping["gdpr"] = "Article 32 (Security of Processing) & Article 25 (Privacy by Design)"
            mapping["ccpa_cpra"] = "Section 1798.100 (Data Minimization & Purpose Limitation)"
            tracks.extend(["Data_Privacy", "Statutory_Legal"])
            
        # 2. Access Control Overlays
        elif any(target in clean_id for target in ["5.15", "5.16", "5.17", "5.18", "8.2", "8.3", "8.5"]):
            mapping["gdpr"] = "Article 32 (Access minimization and identity isolation)"
            mapping["ccpa_cpra"] = "Section 1798.100 (Reasonable security procedures for identity controls)"
            tracks.append("Data_Privacy")
            
        # 3. Critical Infrastructure & Incident Overlays (NIS2)
        if any(target in clean_id for target in ["5.24", "5.25", "5.26", "5.27", "5.28", "6.8", "8.16"]):
            mapping["nis2"] = "Article 21 (Incident Handling, Threat Reporting & Crisis Management)"
            tracks.extend(["Infrastructure_Resilience", "Statutory_Legal"])
        elif "SR" in domain or any(target in clean_id for target in ["5.19", "5.20", "5.21", "5.22", "8.30"]):
            mapping["nis2"] = "Article 21(2)(d) (Supply Chain Security for Information Systems)"
            tracks.extend(["Infrastructure_Resilience", "Statutory_Legal"])

    elif framework_type == "ISO_42001":
        tracks.append("AI_Safety")
        # 1. Impact Assessments & Systems Mapping
        if "A.5" in clean_id:
            mapping["eu_ai_act"] = "Article 9 (Risk Management System for High-Risk AI)"
            mapping["colorado_ai_act"] = "Section 6 (Mandatory Algorithmic Discrimination Impact Assessments)"
            mapping["gdpr"] = "Article 35 (Data Protection Impact Assessment - DPIA for Profiling)"
            tracks.extend(["Statutory_Legal", "Algorithmic_Accountability"])
            
        # 2. Technical Traceability & System Auditing (Logging)
        elif "A.6.8" in clean_id or "A.6.6" in clean_id:
            mapping["eu_ai_act"] = "Article 12 (Automatic Logging & Continuous Traceability)"
            mapping["nis2"] = "Article 21 (Cybersecurity risk-management logging measures)"
            tracks.extend(["Statutory_Legal", "Infrastructure_Resilience"])
            
        # 3. System Transparency and Disclosures
        elif "A.8" in clean_id:
            mapping["eu_ai_act"] = "Article 13 (Transparency and Provision of Information to Users)"
            mapping["ftc_act_sec_5"] = "Section 5 Guidelines (Deceptive AI Claims & Enforcement of Explained Outputs)"
            tracks.extend(["Statutory_Legal", "Algorithmic_Accountability"])
            
        # 4. Human-in-the-Loop Override Structures
        elif "A.9.2" in clean_id:
            mapping["eu_ai_act"] = "Article 14 (Human Oversight Primitives & Built-in Interventions)"
            mapping["colorado_ai_act"] = "Section 4 (Deployer Oversight Controls to Prevent Algorithmic Bias)"
            tracks.extend(["Statutory_Legal", "Algorithmic_Accountability"])
            
        # 5. Data Quality, Bias, & Sourcing
        elif "A.7" in clean_id:
            mapping["eu_ai_act"] = "Article 10 (Data Governance, Ingestion Validation, and Bias Mitigation)"
            mapping["gdpr"] = "Article 22 (Automated individual decision-making exemptions & profiling protections)"
            mapping["ftc_act_sec_5"] = "Section 5 Guidelines (Algorithmic Unfairness stemming from biased dataset feeds)"
            tracks.extend(["Data_Privacy", "Statutory_Legal", "Algorithmic_Accountability"])

    # Fallback to general statements if no strict regulatory overlap triggers
    if not mapping:
        mapping["general_legal_standing"] = "Evaluated as general organizational security governance hygiene under global statutes."
        
    return mapping, list(set(tracks))

def create_semantic_narrative_27001(row, reg_map):
    """Synthesizes controls and regulatory overlays into a dense vector string."""
    return (
        f"Control Crosswalk: ISO 27001:2022 Control {row.get('ISO 27001:2022 Control ID')} "
        f"({row.get('ISO 27001:2022 Control Name')}) mirrors NIST SP 800-53 Rev 5 {row.get('NIST 800-53 Rev 5 Control ID')}. "
        f"ISO mandate summary: {row.get('ISO Control Summary (Paraphrased)')} "
        f"NIST engineering parameter: {row.get('NIST Control Summary (Paraphrased)')} "
        f"Regulatory legal touchpoints: {json.dumps(reg_map)}. "
        f"Framework gap validation: {row.get('Completeness & Gap Analysis')}"
    )

def create_semantic_narrative_42001(row, reg_map):
    """Synthesizes AI controls and complex compliance targets into a dense vector string."""
    return (
        f"AI Governance Crosswalk: ISO/IEC 42001:2023 Control {row.get('ISO 42001 ID')} "
        f"({row.get('ISO 42001 Control Name')}) aligns with {row.get('Target NIST Framework')} {row.get('NIST Control/Category ID')}. "
        f"ISO technical requirement: {row.get('ISO Paraphrased Summary')} "
        f"NIST baseline target: {row.get('NIST Paraphrased Summary')} "
        f"Statutory legislation dependencies: {json.dumps(reg_map)}. "
        f"Framework gap validation: {row.get('Completeness & Gap Analysis')}"
    )

def generate_keywords(domain, name, summary):
    clean_text = f"{domain} {name} {summary}".lower()
    keywords = []
    mapping_hooks = {
        "access": ["access control", "permissions", "rbac", "authentication", "credentials", "identity management"],
        "policy": ["governance", "policy", "framework", "charter", "organizational directives"],
        "data": ["data lifecycle", "provenance", "privacy", "datasets", "pii", "lineage", "masking", "bias"],
        "drift": ["model decay", "drift monitoring", "performance drop", "mlops telemetry", "logging"],
        "vulnerability": ["patch management", "scanning", "vulnerability discovery", "remediation"],
        "physical": ["facility security", "perimeter", "surveillance", "locks", "badge access"],
        "supplier": ["third-party risk", "vendor sla", "supply chain", "scrm", "outsourced development", "api verification"]
    }
    for key, hooks in mapping_hooks.items():
        if key in clean_text:
            keywords.extend(hooks)
    keywords = list(set(keywords))
    return keywords if keywords else ["compliance baseline"]

def determine_asset_target(domain_text, summary_text):
    combined = (domain_text + " " + summary_text).lower()
    if any(word in combined for word in ["human", "personnel", "training", "whistleblower", "staff", "employment"]):
        return "Personnel"
    if any(word in combined for word in ["data", "dataset", "lineage", "pii", "privacy", "records", "masking", "labeling"]):
        return "Datasets"
    if any(word in combined for word in ["hardware", "gpu", "compute", "physical", "perimeter", "facility", "cabling", "utilities"]):
        return "Compute_Infrastructure"
    return "Software_Code"

def transform_csv_to_jsonl(input_csv, output_jsonl, framework_type):
    if not os.path.exists(input_csv):
        print(f"⚠️ Skipping: '{input_csv}' was not found.")
        return

    print(f"⚙️ Compiling {input_csv} with active Regulatory Overlays...")
    records_processed = 0

    with open(input_csv, mode='r', encoding='utf-8') as csv_file:
        reader = csv.DictReader(csv_file)
        
        with open(output_jsonl, mode='w', encoding='utf-8') as jsonl_file:
            for row in reader:
                row = {k.strip(): v for k, v in row.items() if k is not None}
                
                if framework_type == "ISO_27001":
                    iso_id = row.get("ISO 27001:2022 Control ID")
                    iso_name = row.get("ISO 27001:2022 Control Name")
                    iso_summary = row.get("ISO Control Summary (Paraphrased)")
                    nist_id = row.get("NIST 800-53 Rev 5 Control ID")
                    nist_name = row.get("NIST 800-53 Control Name")
                    gap_analysis = row.get("Completeness & Gap Analysis")
                    family = "Traditional_Infra_Security"
                    primary_std = "ISO_27001_2022"
                    domain = nist_id.split("-")[0] if nist_id else "GEN"
                    
                    reg_map, compliance_tracks = get_regulatory_overlay(framework_type, iso_id, domain)
                    text_to_embed = create_semantic_narrative_27001(row, reg_map)
                    
                elif framework_type == "ISO_42001":
                    iso_id = row.get("ISO 42001 ID")
                    iso_name = row.get("ISO 42001 Control Name")
                    iso_summary = row.get("ISO Paraphrased Summary")
                    nist_id = row.get("NIST Control/Category ID")
                    nist_name = row.get("NIST Control/Category Name")
                    gap_analysis = row.get("Completeness & Gap Analysis")
                    family = "AI_Governance"
                    primary_std = "ISO_42001_2023"
                    domain = row.get("Target NIST Framework", "AI_RMF")
                    
                    reg_map, compliance_tracks = get_regulatory_overlay(framework_type, iso_id, domain)
                    text_to_embed = create_semantic_narrative_42001(row, reg_map)
                else:
                    continue

                match_status = "Full" if "full" in str(gap_analysis).lower() else "Partial"
                asset_target = determine_asset_target(domain, iso_summary)
                semantic_hooks = generate_keywords(domain, iso_name, iso_summary)

                json_package = {
                    "id": f"RAG_{primary_std}_{iso_id.replace('.', '_')}",
                    "text_to_embed": text_to_embed,
                    "metadata": {
                        "framework_family": family,
                        "primary_standard": primary_std,
                        "iso_id": iso_id,
                        "iso_name": iso_name,
                        "nist_id": nist_id,
                        "nist_name": nist_name,
                        "match_status": match_status,
                        "control_domain": domain,
                        "semantic_hooks": semantic_hooks,
                        "asset_target": asset_target,
                        "regulatory_mapping": reg_map,
                        "compliance_tracks": compliance_tracks
                    },
                    "llm_context": {
                        "evaluation_checklist": f"Verify if the target corporate policy text satisfies the specific core mandate of {iso_id} regarding: {iso_name}.",
                        "gap_analysis": gap_analysis,
                        "remediation_boilerplate": f"Remediation Action: Ensure the organizational policy explicitly covers parameters defined in {nist_id} ({nist_name}) and associated legal tags: {list(reg_map.keys())}."
                    }
                }

                jsonl_file.write(json.dumps(json_package, ensure_ascii=False) + "\n")
                records_processed += 1
                
    print(f"🎉 Success! Generated '{output_jsonl}' with embedded legal mapping schemas.\n")

if __name__ == "__main__":
    print("🚀 Initiating RAG Knowledge Base Transformation Pipeline with Regulatory Overlays...\n")
    
    transform_csv_to_jsonl(
        input_csv="iso_27001_2022_to_nist_800_53_rev5_mapping.csv",
        output_jsonl="rag_ready_iso_27001_to_nist_800_53.jsonl",
        framework_type="ISO_27001"
    )
    
    transform_csv_to_jsonl(
        input_csv="iso_42001_2023_to_nist_ecosystem_mapping.csv",
        output_jsonl="rag_ready_iso_42001_to_nist_ecosystem.jsonl",
        framework_type="ISO_42001"
    )
    
    print("🏁 Pipeline execution complete. Knowledge bases are fully enriched with statutory legal data blocks.")