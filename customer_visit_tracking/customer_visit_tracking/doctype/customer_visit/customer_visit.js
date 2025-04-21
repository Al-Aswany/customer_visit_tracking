// Copyright (c) 2025, Al-Aswany and contributors
// For license information, please see license.txt

frappe.ui.form.on('Customer Visit', {
    refresh: function(frm) {
        // Disable fields when the document is in Approved state
        if (frm.doc.workflow_state === "Approved") {
            frm.set_df_property('customer', 'read_only', 1);
            frm.set_df_property('visit_date', 'read_only', 1);
            frm.set_df_property('purpose', 'read_only', 1);
            frm.set_df_property('notes', 'read_only', 1);
        } else {
            frm.set_df_property('customer', 'read_only', 0);
            frm.set_df_property('visit_date', 'read_only', 0);
            frm.set_df_property('purpose', 'read_only', 0);
            frm.set_df_property('notes', 'read_only', 0);
        }
        
        // Add a custom button to check completeness
        if (frm.doc.workflow_state !== "Approved") {
            frm.add_custom_button(__('Check Completeness'), function() {
                if (!frm.doc.notes) {
                    frappe.msgprint({
                        title: __('Incomplete Information'),
                        indicator: 'orange',
                        message: __('Please add notes before submitting for review.')
                    });
                } else {
                    frappe.msgprint({
                        title: __('Complete'),
                        indicator: 'green',
                        message: __('All required information is complete.')
                    });
                }
            });
        }
    },
    
    // Add validation before saving
    validate: function(frm) {
        if (frm.doc.workflow_state === "Under Review" && !frm.doc.notes) {
            frappe.validated = false;
            frappe.throw(__("Notes are required before submitting for review."));
        }
    }
});