import frappe


@frappe.whitelist()
def get_customer_visits(customer=None):
    #Retrieve customer visits for a specific customer
    filters = {}
    if customer:
        filters["customer"] = customer
    
    visits = frappe.get_all(
        "Customer Visit",
        filters=filters,
        fields=["name", "customer", "visit_date", "purpose", "notes", "workflow_state"]
    )
    
    return visits