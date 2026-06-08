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
        r"(?i)ignore\s+(all\s+)?previous\s+(instructions|directions)",
        r"(?i)you\s+are\s+now",
        r"(?i)system\s+prompt",
        r"(?i)bypass\s+controls",
        r"(?i)forget\s+rules",
        r"(?i)new\s+persona"
    ]

    for pattern in adversarial_patterns:
        if re.search(pattern, raw_text):
            raise SanitizationError("Adversarial context manipulation or prompt injection detected.")

    return raw_text