# Copyright (c) 2024, Your Company and contributors
# For license information, please see license.txt

import frappe
from frappe.model.document import Document


class CustomerFeedback(Document):
    """Controller for Customer Feedback DocType"""
    
    def validate(self):
        """Validate before saving"""
        self.validate_rating()
        self.set_priority()
    
    def validate_rating(self):
        """Ensure rating is between 1-5"""
        if self.rating:
            rating_num = int(self.rating)
            if rating_num < 1 or rating_num > 5:
                frappe.throw("Rating must be between 1 and 5")
    
    def set_priority(self):
        """Auto-set priority based on rating"""
        if not self.rating:
            return
            
        rating_num = int(self.rating)
        if rating_num <= 2:
            self.priority = "High"
        elif rating_num == 3:
            self.priority = "Medium"
        else:
            self.priority = "Low"
    
    def on_submit(self):
        """Actions after submit"""
        self.notify_team()
    
    def notify_team(self):
        """Send notification to customer service team for low ratings"""
        if not self.rating:
            return
            
        rating_num = int(self.rating)
        if rating_num <= 2:
            # Send email to customer service team
            try:
                frappe.sendmail(
                    recipients=["support@company.com"],
                    subject=f"Low Rating Feedback Alert: {self.name}",
                    message=f"""
                    <p>A customer has submitted low rating feedback:</p>
                    <ul>
                        <li><strong>Feedback ID:</strong> {self.name}</li>
                        <li><strong>Customer:</strong> {self.customer} ({self.customer_name})</li>
                        <li><strong>Rating:</strong> {self.rating}/5</li>
                        <li><strong>Category:</strong> {self.category}</li>
                        <li><strong>Date:</strong> {self.feedback_date}</li>
                    </ul>
                    <p><strong>Feedback:</strong></p>
                    <p>{self.feedback_text}</p>
                    <p>Please review and respond promptly.</p>
                    """,
                    now=True
                )
            except Exception as e:
                frappe.log_error(f"Failed to send notification email: {str(e)}")


def validate(doc, method):
    """Hook function for validate event"""
    pass


def on_submit(doc, method):
    """Hook function for on_submit event"""
    pass
