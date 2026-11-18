import frappe
from frappe.utils import flt


def make_gl_entries(doc, entries):
    """Create one GL Entry per dict in entries (account, debit, credit, party, due_date)."""
    for e in entries:
        frappe.get_doc(
            {
                "doctype": "GL Entry",
                "posting_date": doc.posting_date,
                "due_date": e.get("due_date"),
                "party": e.get("party"),
                "account": e["account"],
                "debit_amount": flt(e.get("debit")),
                "credit_amount": flt(e.get("credit")),
                "is_cancelled": 0,
                "voucher_type": doc.doctype,
                "voucher_number": doc.name,
            }
        ).insert(ignore_permissions=True)


def make_reverse_gl_entries(doc):
    """Mark the original rows as cancelled and add opposite rows (debit and credit swapped)."""
    rows = frappe.get_all(
        "GL Entry",
        filters={
            "voucher_type": doc.doctype,
            "voucher_number": doc.name,
            "is_cancelled": 0,
        },
        fields=["name", "posting_date", "due_date", "party", "account", "debit_amount", "credit_amount"],
    )
    for r in rows:
        frappe.db.set_value("GL Entry", r.name, "is_cancelled", 1, update_modified=False)
        frappe.get_doc(
            {
                "doctype": "GL Entry",
                "posting_date": r.posting_date,
                "due_date": r.due_date,
                "party": r.party,
                "account": r.account,
                "debit_amount": flt(r.credit_amount),
                "credit_amount": flt(r.debit_amount),
                "is_cancelled": 1,
                "voucher_type": doc.doctype,
                "voucher_number": doc.name,
            }
        ).insert(ignore_permissions=True)
