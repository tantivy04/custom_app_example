"""Permission query conditions for Custom App Example"""

import frappe


def get_permission_query_conditions(user=None):
    """Restrict Customer Feedback visibility based on user role.

    - Administrators and System Managers see all records.
    - Other users only see their own submitted feedback.
    """
    if not user:
        user = frappe.session.user

    if "System Manager" in frappe.get_roles(user):
        return ""

    # Non-admins only see records they created
    return f"`tabCustomer Feedback`.`owner` = {frappe.db.escape(user)}"
