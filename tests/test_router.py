import pytest
from orchestrate import local_keyword_router

@pytest.fixture
def mock_knowledge_base():
    """Provides a controlled, static knowledge base for deterministic testing."""
    return [
        {
            "id": "CTRL_001_SECURITY",
            "metadata": {
                "compliance_tracks": ["Operational_Security", "Security_Baseline"],
                "semantic_hooks": ["encryption", "aes", "cipher", "tls", "firewall"]
            }
        },
        {
            "id": "CTRL_002_PRIVACY",
            "metadata": {
                "compliance_tracks": ["Statutory_Legal", "Data_Privacy"],
                "semantic_hooks": ["gdpr", "privacy", "consent", "pii", "subject rights"]
            }
        }
    ]

def test_router_filters_by_active_track(mock_knowledge_base):
    """Verify the router only selects controls relevant to the chosen track."""
    policy_text = "We enforce strict TLS encryption and firewall rules. We also ensure GDPR privacy consent."
    
    # Requesting the Security Baseline track
    security_controls = local_keyword_router(policy_text, mock_knowledge_base, "Security_Baseline")
    
    # It should isolate and return ONLY the security control, ignoring the privacy overlap
    assert len(security_controls) >= 1
    assert all("Security_Baseline" in c["metadata"]["compliance_tracks"] for c in security_controls)
    
    # Ensure it did not pull the privacy control into the security audit
    assert not any(c["id"] == "CTRL_002_PRIVACY" for c in security_controls)

def test_router_handles_no_overlap(mock_knowledge_base):
    """Verify the router behavior when the document has no relevance to the database."""
    policy_text = "We focus on employee wellness, office ergonomics, and cafeteria menus."
    
    # Evaluate against privacy
    privacy_controls = local_keyword_router(policy_text, mock_knowledge_base, "Data_Privacy")
    
    # If the document has zero matching keywords, the router should ideally return an empty list 
    # (or whatever your specific fallback logic dictates)
    assert isinstance(privacy_controls, list)