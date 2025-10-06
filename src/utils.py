"""
Utility functions for the Fake News Detector app
"""


import re


def validate_input(claim: str) -> bool:
    """
    Validate user input claim

    Args:
        claim: The claim to validate

    Returns:
        True if valid, False otherwise
    """
    if not claim or len(claim.strip()) < 10:
        return False

    # Check if it's not just special characters
    if not re.search(r'[a-zA-Z0-9]', claim):
        return False

    return True
