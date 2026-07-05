"""Utility functions for Custom App Example"""


def format_feedback_rating(rating):
    """Convert numeric rating to star display string.

    Usage in Jinja templates: {{ format_feedback_rating(doc.rating) }}
    """
    try:
        rating = int(rating)
    except (TypeError, ValueError):
        return "N/A"

    stars = "★" * rating + "☆" * (5 - rating)
    labels = {1: "Very Poor", 2: "Poor", 3: "Average", 4: "Good", 5: "Excellent"}
    label = labels.get(rating, "")
    return f"{stars} ({label})"
