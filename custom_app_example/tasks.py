"""Scheduled tasks for Custom App Example"""

import frappe


def send_daily_feedback_report():
    """Send a daily summary of customer feedback to the support team."""
    from_date = frappe.utils.add_days(frappe.utils.today(), -1)

    feedbacks = frappe.get_all(
        "Customer Feedback",
        filters={"creation": [">=", from_date]},
        fields=["name", "customer", "rating", "status"],
    )

    if not feedbacks:
        return

    # Log summary — replace with actual email logic as needed
    frappe.logger().info(
        f"Daily Feedback Report: {len(feedbacks)} feedback(s) received since {from_date}"
    )


def cleanup_old_feedbacks():
    """Archive or clean up resolved feedbacks older than 90 days."""
    cutoff = frappe.utils.add_days(frappe.utils.today(), -90)

    old_feedbacks = frappe.get_all(
        "Customer Feedback",
        filters={"status": "Closed", "modified": ["<", cutoff]},
        fields=["name"],
    )

    for fb in old_feedbacks:
        frappe.logger().info(f"Old closed feedback: {fb['name']}")

    frappe.logger().info(
        f"Cleanup: found {len(old_feedbacks)} closed feedback(s) older than {cutoff}"
    )
