"""Hooks configuration for Custom App Example"""

app_name = "custom_app_example"
app_title = "Custom App Example"
app_publisher = "Your Company"
app_description = "Example custom app for ERPNext multi-tenant setup"
app_icon = "octicon octicon-file-directory"
app_color = "grey"
app_email = "support@company.com"
app_license = "MIT"

# Includes in <head>
# app_include_css = "/assets/custom_app_example/css/custom_app_example.css"
# app_include_js = "/assets/custom_app_example/js/custom_app_example.js"

# Document Events
doc_events = {
    "Customer Feedback": {
        "validate": "custom_app_example.custom_app_example.doctype.customer_feedback.customer_feedback.validate",
        "on_submit": "custom_app_example.custom_app_example.doctype.customer_feedback.customer_feedback.on_submit"
    }
}

# Scheduled Tasks
scheduler_events = {
    "daily": [
        "custom_app_example.tasks.send_daily_feedback_report"
    ],
    "weekly": [
        "custom_app_example.tasks.cleanup_old_feedbacks"
    ]
}

# Web pages
website_route_rules = [
    {"from_route": "/feedback/<customer>", "to_route": "custom_feedback_form"},
]

# Jinja customization
jinja = {
    "methods": [
        "custom_app_example.utils.format_feedback_rating"
    ]
}

# Custom permission queries
permission_query_conditions = {
    "Customer Feedback": "custom_app_example.permissions.get_permission_query_conditions"
}

# Installation
# before_install = "custom_app_example.install.before_install"
# after_install = "custom_app_example.install.after_install"

# Desk Notifications
# notification_config = "custom_app_example.notifications.get_notification_config"

# Fixtures
fixtures = [
    {"dt": "Custom Field", "filters": [["module", "in", [app_name]]]},
]
