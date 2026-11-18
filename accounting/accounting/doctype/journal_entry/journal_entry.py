import frappe
from frappe.model.document import Document
from frappe.utils import flt

from accounting.general_ledger import make_gl_entries, make_reverse_gl_entries


class JournalEntry(Document):
    def validate(self):
        self.validate_rows()
        self.calculate_totals()
        self.validate_balance()

    def validate_rows(self):
        if len(self.accounts) < 2:
            frappe.throw("Add at least two rows in Accounting Entries")

        for row in self.accounts:
            if flt(row.debit) < 0 or flt(row.credit) < 0:
                frappe.throw(f"Row {row.idx}: Debit and Credit cannot be negative")
            if flt(row.debit) and flt(row.credit):
                frappe.throw(f"Row {row.idx}: Enter either Debit or Credit, not both")
            if not flt(row.debit) and not flt(row.credit):
                frappe.throw(f"Row {row.idx}: Enter a Debit or a Credit amount")

    def calculate_totals(self):
        self.total_debit = sum(flt(row.debit) for row in self.accounts)
        self.total_credit = sum(flt(row.credit) for row in self.accounts)
        self.difference = flt(self.total_debit) - flt(self.total_credit)

    def validate_balance(self):
        if abs(flt(self.difference)) > 0.005:
            frappe.throw(f"Total Debit must equal Total Credit. Difference is {self.difference}")

    def on_submit(self):
        make_gl_entries(
            self,
            [
                {
                    "account": row.account,
                    "debit": row.debit,
                    "credit": row.credit,
                    "party": row.party,
                }
                for row in self.accounts
            ],
        )

    def on_cancel(self):
        self.ignore_linked_doctypes = ("GL Entry",)
        make_reverse_gl_entries(self)
