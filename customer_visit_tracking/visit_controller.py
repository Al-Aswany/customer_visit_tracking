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
    
    return incomplete_visits