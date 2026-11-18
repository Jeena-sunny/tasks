import frappe
from frappe.model.document import Document
from frappe.utils import flt


class PaymentEntry(Document):
	def validate(self):
		if flt(self.amount) <= 0:
			frappe.throw("Amount must be greater than zero")

		if self.account_paid_from == self.account_paid_to:
			frappe.throw("Account Paid From and Account Paid To cannot be the same")

		self.validate_party()

	def validate_party(self):
		party_type = frappe.db.get_value("Party", self.party, "party_type")
		if party_type != self.party_type:
			frappe.throw(f"{self.party} is a {party_type}, not a {self.party_type}")

		if self.payment_type == "Receive" and self.party_type != "Customer":
			frappe.throw("Receive payments must be from a Customer")
		if self.payment_type == "Pay" and self.party_type != "Supplier":
			frappe.throw("Pay payments must be made to a Supplier")
