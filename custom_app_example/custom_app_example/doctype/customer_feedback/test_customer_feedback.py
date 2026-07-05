# Copyright (c) 2024, Your Company and contributors
# For license information, please see license.txt

import frappe
import unittest


class TestCustomerFeedback(unittest.TestCase):

    def setUp(self):
        """Create a test customer if not exists"""
        if not frappe.db.exists("Customer", "_Test Feedback Customer"):
            customer = frappe.get_doc({
                "doctype": "Customer",
                "customer_name": "_Test Feedback Customer",
                "customer_type": "Individual",
                "customer_group": "All Customer Groups",
                "territory": "All Territories",
            })
            customer.insert(ignore_permissions=True)
            frappe.db.commit()

    def tearDown(self):
        """Clean up test records"""
        frappe.db.delete("Customer Feedback", {"customer": "_Test Feedback Customer"})
        frappe.db.commit()

    def make_feedback(self, rating, feedback_text="Test feedback"):
        doc = frappe.get_doc({
            "doctype": "Customer Feedback",
            "naming_series": "CUST-FB-.YYYY.-",
            "customer": "_Test Feedback Customer",
            "rating": str(rating),
            "feedback_text": feedback_text,
            "category": "Product Quality",
        })
        doc.insert(ignore_permissions=True)
        return doc

    # ── Priority auto-set ────────────────────────────────────────────────────

    def test_priority_high_for_low_rating(self):
        """Rating 1 → Priority High"""
        doc = self.make_feedback(1)
        self.assertEqual(doc.priority, "High")

    def test_priority_high_for_rating_2(self):
        """Rating 2 → Priority High"""
        doc = self.make_feedback(2)
        self.assertEqual(doc.priority, "High")

    def test_priority_medium_for_rating_3(self):
        """Rating 3 → Priority Medium"""
        doc = self.make_feedback(3)
        self.assertEqual(doc.priority, "Medium")

    def test_priority_low_for_rating_4(self):
        """Rating 4 → Priority Low"""
        doc = self.make_feedback(4)
        self.assertEqual(doc.priority, "Low")

    def test_priority_low_for_rating_5(self):
        """Rating 5 → Priority Low"""
        doc = self.make_feedback(5)
        self.assertEqual(doc.priority, "Low")

    # ── Default status ───────────────────────────────────────────────────────

    def test_default_status_is_new(self):
        """Newly created feedback status should be New"""
        doc = self.make_feedback(4)
        self.assertEqual(doc.status, "New")

    # ── API: submit_feedback_api ─────────────────────────────────────────────

    def test_api_submit_feedback_success(self):
        """submit_feedback_api returns success and creates document"""
        from custom_app_example.api.v1 import submit_feedback_api

        result = submit_feedback_api(
            customer="_Test Feedback Customer",
            rating="4",
            feedback_text="API test feedback",
            category="Delivery",
        )
        self.assertTrue(result.get("success"))
        self.assertIn("feedback_id", result)
        self.assertTrue(frappe.db.exists("Customer Feedback", result["feedback_id"]))

    def test_api_submit_invalid_rating(self):
        """submit_feedback_api with rating > 5 should return error"""
        from custom_app_example.api.v1 import submit_feedback_api

        result = submit_feedback_api(
            customer="_Test Feedback Customer",
            rating="9",
            feedback_text="Bad rating test",
        )
        self.assertFalse(result.get("success"))

    # ── API: get_feedback_analytics ──────────────────────────────────────────

    def test_analytics_returns_expected_keys(self):
        """get_feedback_analytics should return required keys"""
        from custom_app_example.api.v1 import get_feedback_analytics

        self.make_feedback(5)
        result = get_feedback_analytics()
        for key in ["total_feedbacks", "average_rating", "category_breakdown",
                    "status_breakdown", "priority_breakdown"]:
            self.assertIn(key, result)

    # ── API: get_customer_feedback_history ───────────────────────────────────

    def test_feedback_history_for_customer(self):
        """get_customer_feedback_history should return created feedbacks"""
        from custom_app_example.api.v1 import get_customer_feedback_history

        self.make_feedback(3)
        self.make_feedback(5)
        result = get_customer_feedback_history("_Test Feedback Customer")
        self.assertTrue(result.get("success"))
        self.assertGreaterEqual(result["count"], 2)
