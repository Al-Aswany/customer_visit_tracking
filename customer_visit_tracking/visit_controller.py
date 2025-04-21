import frappe


@frappe.whitelist()
def check_incomplete_visits():
    """Check for visits with missing notes and notify owners"""
    incomplete_visits = frappe.get_all(
        "Customer Visit",
        filters={"notes": ["is", "not set"], "workflow_state": ["!=", "Draft"]},
        fields=["name", "customer", "visit_date", "owner"]
    )
    
    for visit in incomplete_visits:
        user = frappe.get_doc("User", visit.owner)
        
        # Send email notification
        frappe.sendmail(
            recipients=[user.email],
            subject=f"Incomplete Visit Data: {visit.name}",
            message=f"""
            <p>Dear {user.full_name},</p>
            <p>The customer visit {visit.name} for {visit.customer} on {visit.visit_date} is missing notes.</p>
            <p>Please complete this information at your earliest convenience.</p>
            """
        )
        
        # Log the notification
        frappe.log_error(
            title="Incomplete Visit Notification",
            message=f"Notification sent for visit {visit.name} to {user.email}"
        )
    
    return incomplete_visits


def notify_manager_on_approval(doc):
    """Notify manager when a visit is approved"""
    managers = frappe.get_all(
        "User",
        filters={"role": "Sales Manager"},
        fields=["email", "full_name"]
    )
    
    for manager in managers:
        frappe.sendmail(
            recipients=[manager.email],
            subject=f"Visit Approved: {doc.name}",
            message=f"""
            <p>Dear {manager.full_name},</p>
            <p>The customer visit {doc.name} for {doc.customer} has been approved.</p>
            <p>Visit Details:</p>
            <ul>
                <li>Date: {doc.visit_date}</li>
                <li>Purpose: {doc.purpose}</li>
            </ul>
            """
        )