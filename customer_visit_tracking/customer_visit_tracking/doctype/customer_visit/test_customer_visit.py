# Copyright (c) 2025, Al-Aswany and Contributors
# See license.txt


import unittest
import frappe
from frappe.utils import getdate, add_days

class TestCustomerVisit(unittest.TestCase):
    def setUp(self):
        # Create a test customer
        if not frappe.db.exists("Customer", "_Test Customer for Visit"):
            customer = frappe.get_doc({
                "doctype": "Customer",
                "customer_name": "_Test Customer for Visit",
                "customer_group": "Commercial",
                "territory": "All Territories",
                "customer_type": "Company"
            })
            customer.insert(ignore_permissions=True)
            
        # Create a test user with Sales User role if not exists
        if not frappe.db.exists("User", "test_sales_user@example.com"):
            user = frappe.get_doc({
                "doctype": "User",
                "email": "test_sales_user@example.com",
                "first_name": "Test",
                "last_name": "Sales User",
                "roles": [{"role": "Sales User"}],
                "user_type": "System User"
            })
            user.insert(ignore_permissions=True)
            
        # Create a test user with Sales Manager role if not exists
        if not frappe.db.exists("User", "test_sales_manager@example.com"):
            user = frappe.get_doc({
                "doctype": "User",
                "email": "test_sales_manager@example.com",
                "first_name": "Test",
                "last_name": "Sales Manager",
                "roles": [{"role": "Sales Manager"}],
                "user_type": "System User"
            })
            user.insert(ignore_permissions=True)
    
    def tearDown(self):
        # Delete test visits
        for visit in frappe.get_all("Customer Visit", filters={"customer": "_Test Customer for Visit"}):
            frappe.delete_doc("Customer Visit", visit.name, force=1, ignore_permissions=True)
    
    def test_create_customer_visit(self):
        """Test creating a customer visit"""
        frappe.set_user("test_sales_user@example.com")
        
        visit = frappe.get_doc({
            "doctype": "Customer Visit",
            "customer": "_Test Customer for Visit",
            "visit_date": getdate(),
            "purpose": "Meeting"
        })
        visit.insert()
        
        self.assertEqual(visit.workflow_state, "Draft")
        self.assertEqual(visit.customer, "_Test Customer for Visit")
        
    def test_workflow_transitions(self):
        """Test workflow transitions"""
        # Create a visit as Sales User
        frappe.set_user("test_sales_user@example.com")
        
        visit = frappe.get_doc({
            "doctype": "Customer Visit",
            "customer": "_Test Customer for Visit",
            "visit_date": getdate(),
            "purpose": "Meeting",
            "notes": "Test notes for the meeting"
        })
        visit.insert()
        
        # Transition to Under Review
        visit.workflow_state = "Under Review"
        visit.save()
        
        # Switch to Sales Manager to approve
        frappe.set_user("test_sales_manager@example.com")
        
        # Get the updated doc
        visit = frappe.get_doc("Customer Visit", visit.name)
        
        # Transition to Approved
        visit.workflow_state = "Approved"
        visit.save()
        
        # Verify final state
        visit = frappe.get_doc("Customer Visit", visit.name)
        self.assertEqual(visit.workflow_state, "Approved")
        
    def test_api_endpoint(self):
        """Test the API endpoint for retrieving visits"""
        frappe.set_user("Administrator")
        
        # Create multiple visits
        visit1 = frappe.get_doc({
            "doctype": "Customer Visit",
            "customer": "_Test Customer for Visit",
            "visit_date": getdate(),
            "purpose": "Meeting",
            "notes": "Test notes 1"
        })
        visit1.insert(ignore_permissions=True)
        
        visit2 = frappe.get_doc({
            "doctype": "Customer Visit",
            "customer": "_Test Customer for Visit",
            "visit_date": add_days(getdate(), 1),
            "purpose": "Follow-up",
            "notes": "Test notes 2"
        })
        visit2.insert(ignore_permissions=True)
        
        # Test API endpoint
        from customer_visit_tracking.api import get_customer_visits
        
        visits = get_customer_visits(customer="_Test Customer for Visit")
        self.assertEqual(len(visits), 2)
        
    def test_validation(self):
        """Test validation for required notes"""
        frappe.set_user("test_sales_user@example.com")
        
        # Create a visit without notes
        visit = frappe.get_doc({
            "doctype": "Customer Visit",
            "customer": "_Test Customer for Visit",
            "visit_date": getdate(),
            "purpose": "Meeting"
        })
        visit.insert()
        
        # Try to transition to Under Review without notes
        visit.workflow_state = "Under Review"
        
        # This should raise a validation error
        with self.assertRaises(frappe.ValidationError):
            visit.save()