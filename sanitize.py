import re
import os
import sys

# Custom enterprise dictionary for data masking
COMPANY_SPECIFIC_MARKERS = {
    "Acme Corporation": "[COMPANY_NAME]",
    "AcmeCorp": "[COMPANY_NAME]",
    "Project Genesis": "[PROPRIETARY_PROJECT_NAME]",
    "Project Titan": "[CRITICAL_AI_INFRASTRUCTURE]",
    "NovaCompute": "[PROPRIETARY_MODEL_NAME]",
    "John Doe": "[SENIOR_EXECUTIVE_NAME]",
    "Jane Smith": "[CISO_NAME]",
    "AlphaCluster": "[INTERNAL_COMPUTE_CLUSTER]"
}

def check_prompt_injection_firewall(text):
    """
    ADVERSARIAL INPUT FIREWALL
    Scans incoming untrusted text for malicious structural overrides and jailbreak phrases.
    """
    adversarial_patterns = [
        r"ignore\s+(?:all\s+)?previous\s+instructions",
        r"override\s+(?:the\s+)?system",
        r"disregard\s+(?:all\s+)?prior\s+guidelines",
        r"you\s+are\s+no\s+longer\s+an\s+ai",
        r"bypass\s+(?:the\s+)?compliance\s+checks",
        r"output\s+only\s+the\s+word\s+compliant"
    ]
    
    text_clean = text.lower()
    for pattern in adversarial_patterns:
        if re.search(pattern, text_clean):
            return True, pattern
            
    return False, None

def clean_patterns(text):
    """Masks standard structural PII using regular expressions."""
    email_pattern = r'[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}'
    text = re.sub(email_pattern, '[REDACTED_EMAIL_ADDRESS]', text)
    
    ip_pattern = r'\b\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}\b'
    text = re.sub(ip_pattern, '[INTERNAL_IP_ADDRESS]', text)
    
    phone_pattern = r'\b(?:\+?\d{1,3}[-.\s]?)?\(?\d{3}\)?[-.\s]?\d{3}[-.\s]?\d{4}\b'
    text = re.sub(phone_pattern, '[REDACTED_PHONE_NUMBER]', text)
    
    text = re.sub(r'(/[a-zA-Z0-9_-]+){3,}', '[INTERNAL_SYSTEM_PATH]', text)
    text = re.sub(r'[a-zA-Z]:\\(?:[a-zA-Z0-9_-]+\\)+', '[INTERNAL_SYSTEM_PATH]', text)
    return text

def clean_corporate_keywords(text, lookup_dict):
    """Masks custom proprietary keywords from the dictionary."""
    for keyword, placeholder in lookup_dict.items():
        pattern = re.compile(re.escape(keyword), re.IGNORECASE)
        text = pattern.sub(placeholder, text)
    return text

def sanitize_document(input_filename, output_filename):
    if not os.path.exists(input_filename):
        print(f"⚠️ Error: Could not find '{input_filename}'. Please create it.")
        return

    print(f"🔒 Ingesting raw policy document: '{input_filename}'")
    
    raw_content = ""
    try:
        with open(input_filename, 'r', encoding='utf-8') as infile:
            raw_content = infile.read()
    except UnicodeDecodeError:
        with open(input_filename, 'r', encoding='cp1252', errors='replace') as infile:
            raw_content = infile.read()

    # --- ADVANCED GUARDRAIL PASS: PROMPT INJECTION CHECK ---
    is_compromised, caught_pattern = check_prompt_injection_firewall(raw_content)
    if is_compromised:
        print("\n" + "="*60)
        print(f"🚨 CRITICAL SECURITY BREACH DETECTED IN '{input_filename}'")
        print(f"🛑 FIREWALL ACTION: Input execution aborted.")
        print(f"🔎 REASON: Matched adversarial override pattern -> '{caught_pattern}'")
        print("="*60 + "\n")
        # Gracefully stop script execution before any compromised files are created
        sys.exit("Pipeline terminated due to adversarial input risk state.")
    # --------------------------------------------------------

    print("🛡️ Input verified as clean. Executing data-masking routines...")
    scrubbed_content = clean_patterns(raw_content)
    final_safe_content = clean_corporate_keywords(scrubbed_content, COMPANY_SPECIFIC_MARKERS)

    with open(output_filename, 'w', encoding='utf-8') as outfile:
        outfile.write(final_safe_content)
        
    print(f"✨ Anonymized file saved safely as '{output_filename}'. Ready for routing.\n")

if __name__ == "__main__":
    sanitize_document("raw_policy.txt", "sanitized_policy.txt")