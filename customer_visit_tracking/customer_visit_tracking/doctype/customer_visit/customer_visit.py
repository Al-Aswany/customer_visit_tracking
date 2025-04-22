# Copyright (c) 2025, Al-Aswany and contributors
# For license information, please see license.txt

import frappe
from frappe.model.document import Document
from customer_visit_tracking.utils.socket_helper import emit_via_socket
from customer_visit_tracking.visit_controller import notify_manager_on_approval

class CustomerVisit(Document):
    def on_update(self):
        if self.workflow_state == "Approved":
            notify_manager_on_approval(self)
    

        
            
