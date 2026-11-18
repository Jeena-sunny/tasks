import frappe
from frappe.model.document import Document
from frappe.utils import flt, getdate

from accounting.general_ledger import make_gl_entries, make_reverse_gl_entries


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

    def on_submit(self):
        make_gl_entries(
            self,
            [
                {
                    "account": self.debit_to,
                    "debit": self.total_amount,
                    "party": self.customer,
                    "due_date": self.payment_due_date,
                },
                {"account": self.income_account, "credit": self.total_amount},
            ],
        )

    def on_cancel(self):
        self.ignore_linked_doctypes = ("GL Entry",)
        make_reverse_gl_entries(self)
