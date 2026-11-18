import frappe
from frappe.model.document import Document
from frappe.utils import flt, getdate


class SalesInvoice(Document):
	def validate(self):
		self.validate_dates()
		self.calculate_totals()

	def validate_dates(self):
		if self.payment_due_date and getdate(self.payment_due_date) < getdate(self.posting_date):
			frappe.throw("Payment Due Date cannot be before Posting Date")

	def calculate_totals(self):
		total_qty = 0
		total_amount = 0
		for row in self.items:
			row.amount = flt(row.qty) * flt(row.rate)
			total_qty += flt(row.qty)
			total_amount += flt(row.amount)
		self.total_qty = total_qty
		self.total_amount = total_amount
