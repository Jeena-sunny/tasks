import frappe
from frappe.model.document import Document
from frappe.utils import getdate


class FiscalYear(Document):
	def validate(self):
		if getdate(self.end_date) <= getdate(self.start_date):
			frappe.throw("End Date must be after Start Date")
