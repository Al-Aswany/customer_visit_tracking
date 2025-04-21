# Copyright (c) 2025, Al-Aswany and contributors
# For license information, please see license.txt

import frappe
from frappe.model.document import Document

class CustomerVisit(Document):
	def on_update(self):
		self.check_visit_completeness()
	
	def check_visit_completeness(doc, method):
		"""Check if the visit has all required information and notify if incomplete"""
		if doc.workflow_state in ["Under Review", "Approved"] and not doc.notes:
			user = frappe.get_doc("User", frappe.session.user)
			frappe.msgprint(
				msg=f"Visit {doc.name} is missing notes. Please complete before proceeding.",
				title="Incomplete Visit Data",
				indicator="orange"
			)
			
			# Send email notification
			frappe.sendmail(
				recipients=[user.email],
				subject=f"Incomplete Visit Data: {doc.name}",
				message=f"""
				<p>Dear {user.full_name},</p>
				<p>The customer visit {doc.name} for {doc.customer} on {doc.visit_date} is missing notes.</p>
				<p>Please complete this information at your earliest convenience.</p>
				"""
			)