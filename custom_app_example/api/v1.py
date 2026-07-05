# Copyright (c) 2024, Your Company and contributors
# For license information, please see license.txt

"""API endpoints for Custom App Example"""

import frappe
from frappe import _


@frappe.whitelist()
def send_thank_you_email(feedback_id):
    """Send thank you email to customer
    
    Args:
        feedback_id (str): Customer Feedback document name
        
    Returns:
        dict: Success/error response
    """
    try:
        feedback = frappe.get_doc("Customer Feedback", feedback_id)
        customer = frappe.get_doc("Customer", feedback.customer)
        
        if not customer.email_id:
            frappe.throw(_("Customer email not found"))
        
        frappe.sendmail(
            recipients=[customer.email_id],
            subject=_("Thank you for your feedback"),
            message=f"""
            <p>Dear {customer.customer_name},</p>
            
            <p>Thank you for taking the time to share your valuable feedback with us.</p>
            
            <p>Your input helps us improve our products and services to better serve you.</p>
            
            <p>We appreciate your continued support.</p>
            
            <p>Best regards,<br>
            Customer Service Team</p>
            """,
            now=True
        )
        
        return {
            "success": True,
            "message": _("Email sent successfully")
        }
        
    except Exception as e:
        frappe.log_error(f"Error sending thank you email: {str(e)}")
        return {
            "success": False,
            "message": str(e)
        }


@frappe.whitelist(allow_guest=True)
def submit_feedback_api(customer, rating, feedback_text, category=None):
    """REST API endpoint to submit feedback
    
    Args:
        customer (str): Customer ID
        rating (str): Rating 1-5
        feedback_text (str): Feedback text
        category (str, optional): Feedback category
        
    Returns:
        dict: Feedback submission result
    """
    try:
        # Validate rating
        rating_num = int(rating)
        if rating_num < 1 or rating_num > 5:
            frappe.throw(_("Rating must be between 1 and 5"))
        
        # Create new feedback document
        doc = frappe.get_doc({
            "doctype": "Customer Feedback",
            "customer": customer,
            "rating": str(rating),
            "feedback_text": feedback_text,
            "category": category or "Other",
            "status": "New",
            "naming_series": "CUST-FB-.YYYY.-"
        })
        doc.insert(ignore_permissions=True)
        frappe.db.commit()
        
        return {
            "success": True,
            "feedback_id": doc.name,
            "message": _("Feedback submitted successfully")
        }
        
    except Exception as e:
        frappe.log_error(f"Error submitting feedback: {str(e)}")
        frappe.db.rollback()
        return {
            "success": False,
            "error": str(e),
            "message": _("Failed to submit feedback")
        }


@frappe.whitelist()
def get_feedback_analytics(from_date=None, to_date=None):
    """Get feedback analytics for dashboard
    
    Args:
        from_date (str, optional): Start date filter
        to_date (str, optional): End date filter
        
    Returns:
        dict: Analytics data
    """
    try:
        filters = {}
        if from_date:
            filters["feedback_date"] = [">=", from_date]
        if to_date:
            if "feedback_date" in filters:
                filters["feedback_date"] = ["between", [from_date, to_date]]
            else:
                filters["feedback_date"] = ["<=", to_date]
        
        feedbacks = frappe.get_all(
            "Customer Feedback",
            filters=filters,
            fields=["rating", "category", "status", "priority"]
        )
        
        # Calculate analytics
        total = len(feedbacks)
        if total == 0:
            return {
                "total_feedbacks": 0,
                "average_rating": 0,
                "category_breakdown": {},
                "status_breakdown": {},
                "priority_breakdown": {}
            }
        
        avg_rating = sum(int(f.rating) for f in feedbacks) / total
        
        # Category breakdown
        category_breakdown = {}
        for f in feedbacks:
            category = f.category or "Other"
            category_breakdown[category] = category_breakdown.get(category, 0) + 1
        
        # Status breakdown
        status_breakdown = {}
        for f in feedbacks:
            status = f.status or "New"
            status_breakdown[status] = status_breakdown.get(status, 0) + 1
        
        # Priority breakdown
        priority_breakdown = {}
        for f in feedbacks:
            priority = f.priority or "Low"
            priority_breakdown[priority] = priority_breakdown.get(priority, 0) + 1
        
        return {
            "total_feedbacks": total,
            "average_rating": round(avg_rating, 2),
            "category_breakdown": category_breakdown,
            "status_breakdown": status_breakdown,
            "priority_breakdown": priority_breakdown
        }
        
    except Exception as e:
        frappe.log_error(f"Error getting analytics: {str(e)}")
        return {
            "success": False,
            "error": str(e)
        }


@frappe.whitelist()
def get_customer_feedback_history(customer):
    """Get all feedback history for a customer
    
    Args:
        customer (str): Customer ID
        
    Returns:
        list: List of feedback records
    """
    try:
        feedbacks = frappe.get_all(
            "Customer Feedback",
            filters={"customer": customer},
            fields=["name", "feedback_date", "rating", "category", 
                    "status", "feedback_text", "priority"],
            order_by="feedback_date desc"
        )
        
        return {
            "success": True,
            "feedbacks": feedbacks,
            "count": len(feedbacks)
        }
        
    except Exception as e:
        frappe.log_error(f"Error getting feedback history: {str(e)}")
        return {
            "success": False,
            "error": str(e)
        }
