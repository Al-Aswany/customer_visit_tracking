import frappe
from .utils.socket_helper import emit_via_socket


@frappe.whitelist()
def check_incomplete_visits():
    """Check for visits with missing notes and notify owners"""
    incomplete_visits = frappe.get_all(
        "Customer Visit",
        filters={"notes": ["is", "not set"] },
        fields=["name", "customer", "visit_date", "owner"]
    )
    
    for visit in incomplete_visits:
        user = frappe.get_doc("User", visit.owner)
        
        # Create notification log
        notification = frappe.get_doc({
            "doctype": "Notification Log",
            "subject": f"Incomplete Visit Data: {visit.name}",
            "for_user": user.name,
            "type": "Alert",
            "document_type": "Customer Visit",
            "document_name": visit.name,
            "read": 0,
            "notification_message": f"The customer visit {visit.name} for {visit.customer} is missing notes."
        }).insert(ignore_permissions=True)
        

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
        print(f"Notifying manager: {manager.full_name} ({manager.email})")
        
        # Create notification log
        notification = frappe.get_doc({
            "doctype": "Notification Log",
            "subject": f"Visit Approved: {doc.name}",
            "for_user": manager.name,
            "type": "Alert",
            "document_type": "Customer Visit",
            "document_name": doc.name,
            "read": 0,
            "notification_message": f"The customer visit {doc.name} for {doc.customer} has been approved."
        }).insert(ignore_permissions=True)
        

        
