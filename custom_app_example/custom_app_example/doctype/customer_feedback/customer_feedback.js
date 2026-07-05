// Copyright (c) 2024, Your Company and contributors
// For license information, please see license.txt

frappe.ui.form.on('Customer Feedback', {
    refresh: function(frm) {
        // Add custom button for sending thank you email
        if (!frm.is_new() && frm.doc.customer) {
            frm.add_custom_button(__('Send Thank You Email'), function() {
                frappe.call({
                    method: 'custom_app_example.api.v1.send_thank_you_email',
                    args: {
                        feedback_id: frm.doc.name
                    },
                    callback: function(r) {
                        if (!r.exc) {
                            frappe.msgprint({
                                title: __('Success'),
                                indicator: 'green',
                                message: __('Thank you email sent successfully')
                            });
                        }
                    }
                });
            });
        }

        // Show feedback stats
        if (!frm.is_new()) {
            frm.add_custom_button(__('View Analytics'), function() {
                frappe.set_route('query-report', 'Feedback Analytics');
            });
        }
    },
    
    rating: function(frm) {
        // Show warning for low ratings
        if (frm.doc.rating) {
            let rating_num = parseInt(frm.doc.rating);
            
            if (rating_num <= 2) {
                frappe.msgprint({
                    title: __('Low Rating Alert'),
                    indicator: 'red',
                    message: __('This is a low rating. Please ensure detailed feedback is provided and follow up promptly.')
                });
                
                // Auto-set status to In Review for low ratings
                if (frm.doc.status === 'New') {
                    frm.set_value('status', 'In Review');
                }
            } else if (rating_num >= 4) {
                frappe.msgprint({
                    title: __('Great!'),
                    indicator: 'green',
                    message: __('Thank you for the positive feedback!')
                });
            }
        }
    },
    
    customer: function(frm) {
        // Fetch customer information when customer is selected
        if (frm.doc.customer) {
            frappe.call({
                method: 'frappe.client.get',
                args: {
                    doctype: 'Customer',
                    name: frm.doc.customer
                },
                callback: function(r) {
                    if (r.message) {
                        frm.set_value('customer_name', r.message.customer_name);
                        
                        // Show customer info
                        if (r.message.email_id) {
                            frm.set_intro(__('Customer Email: {0}', [r.message.email_id]), 'blue');
                        }
                    }
                }
            });
        }
    },
    
    status: function(frm) {
        // Auto-fill response details when status changes
        if (frm.doc.status === 'Resolved' || frm.doc.status === 'Closed') {
            if (!frm.doc.responded_by) {
                frm.set_value('responded_by', frappe.session.user);
            }
            if (!frm.doc.response_date) {
                frm.set_value('response_date', frappe.datetime.now_date());
            }
        }
    }
});
