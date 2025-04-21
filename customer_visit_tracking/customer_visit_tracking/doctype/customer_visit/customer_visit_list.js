frappe.listview_settings["Customer Visit"] = {
    onload: function(listview) {
        listview.page.add_inner_button(__("Check Incomplete Visits"), function() {
            frappe.call({
                method: "customer_visit_tracking.visit_controller.check_incomplete_visits",
                callback: function(r) {
                    if (r.message) {
                        frappe.msgprint({
                            title: __("Incomplete Visits"),
                            indicator: "orange",
                            message: __("Found {0} visits with missing information. Notifications have been sent to respective owners.", [r.message.length])
                        });
                    } else {
                        frappe.msgprint({
                            title: __("Complete Visits"),
                            indicator: "green",
                            message: __("All visits have complete information.")
                        });
                    }
                }
            });
        });
    }
};