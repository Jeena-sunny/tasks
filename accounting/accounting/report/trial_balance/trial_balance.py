import frappe


def execute(filters=None):
    filters = filters or {}

    columns = [
        {"label": "Account", "fieldname": "account", "fieldtype": "Link", "options": "Account", "width": 220},
        {"label": "Account Type", "fieldname": "account_type", "fieldtype": "Data", "width": 120},
        {"label": "Debit", "fieldname": "debit", "fieldtype": "Currency", "width": 140},
        {"label": "Credit", "fieldname": "credit", "fieldtype": "Currency", "width": 140},
        {"label": "Balance (Dr - Cr)", "fieldname": "balance", "fieldtype": "Currency", "width": 160},
    ]

    conditions = "gl.is_cancelled = 0"
    values = {}
    if filters.get("from_date"):
        conditions += " AND gl.posting_date >= %(from_date)s"
        values["from_date"] = filters["from_date"]
    if filters.get("to_date"):
        conditions += " AND gl.posting_date <= %(to_date)s"
        values["to_date"] = filters["to_date"]

    data = frappe.db.sql(
        f"""
        SELECT gl.account AS account,
               acc.account_type AS account_type,
               SUM(gl.debit_amount) AS debit,
               SUM(gl.credit_amount) AS credit,
               SUM(gl.debit_amount) - SUM(gl.credit_amount) AS balance
        FROM `tabGL Entry` gl
        LEFT JOIN `tabAccount` acc ON acc.name = gl.account
        WHERE {conditions}
        GROUP BY gl.account, acc.account_type
        ORDER BY gl.account
        """,
        values,
        as_dict=True,
    )
    return columns, data
