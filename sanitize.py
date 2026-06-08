import re

class SanitizationError(Exception):
    """Custom exception raised when an adversarial prompt injection is detected."""
    pass

def sanitize_text(raw_text: str) -> str:
    """
    Evaluates input text for prompt injection attempts,
    jailbreaks, and disallowed control characters.
    """
    if not raw_text or not raw_text.strip():
        raise SanitizationError("Input document is empty or unreadable.")

    # Adversarial pattern matching (Prompt Injection Firewall)
    adversarial_patterns = [
        r"(?i)disregard\s+(all\s+|any\s+|previous\s+|prior\s+)?instructions",
        r"(?i)act\s+as\s+(if\s+you\s+are|an?\s+)",
        r"(?i)jailbreak",
        r"(?i)do\s+not\s+follow",
        r"(?i)override\s+(original\s+|all\s+)?compliance",
        r"(?i)new\s+(system\s+|base\s+|core\s+)?instructions",
        r"(?i)forget\s+(all\s+|your\s+|previous\s+)?instructions"
    ]

    for pattern in adversarial_patterns:
        if re.search(pattern, raw_text):
            raise SanitizationError("Adversarial context manipulation or prompt injection detected.")

    return raw_text