import frappe


def execute(filters=None):
    columns = [
        {"label": "Posting Date", "fieldname": "posting_date", "fieldtype": "Date", "width": 120},
        {"label": "Account", "fieldname": "account", "fieldtype": "Link", "options": "Account", "width": 200},
        {"label": "Party", "fieldname": "party", "fieldtype": "Link", "options": "Party", "width": 150},
        {"label": "Debit Amount", "fieldname": "debit_amount", "fieldtype": "Currency", "width": 130},
        {"label": "Credit Amount", "fieldname": "credit_amount", "fieldtype": "Currency", "width": 130},
        {"label": "Voucher Type", "fieldname": "voucher_type", "fieldtype": "Data", "width": 130},
        {"label": "Voucher No", "fieldname": "voucher_number", "fieldtype": "Data", "width": 160},
    ]

    data = frappe.db.sql(
        """
        SELECT posting_date, account, party, debit_amount, credit_amount,
               voucher_type, voucher_number
        FROM `tabGL Entry`
        WHERE is_cancelled = 0
        ORDER BY posting_date, creation
        """,
        as_dict=True,
    )

    return columns, data
