
import frappe

try:
    from frappe.tests import IntegrationTestCase as BaseTestCase
except ImportError:
    from frappe.tests.utils import FrappeTestCase as BaseTestCase

CASH = "Cash"
SALES = "Sales"


def make_journal_entry(debit_account=CASH, credit_account=SALES, debit=1000, credit=1000):
    return frappe.get_doc(
        {
            "doctype": "Journal Entry",
            "posting_date": "2026-11-18",
            "accounts": [
                {"account": debit_account, "debit": debit, "credit": 0},
                {"account": credit_account, "debit": 0, "credit": credit},
            ],
        }
    )


def gl_rows(voucher_type, voucher_number):
    return frappe.get_all(
        "GL Entry",
        filters={"voucher_type": voucher_type, "voucher_number": voucher_number},
        fields=["account", "debit_amount", "credit_amount", "is_cancelled"],
    )


class TestGLEntry(BaseTestCase):
    def test_gl_entries_created_on_submit(self):
        je = make_journal_entry().insert()
        self.assertEqual(len(gl_rows("Journal Entry", je.name)), 0)

        je.submit()
        rows = gl_rows("Journal Entry", je.name)
        self.assertEqual(len(rows), 2)
        self.assertEqual(sum(r.debit_amount for r in rows), 1000)
        self.assertEqual(sum(r.credit_amount for r in rows), 1000)
        self.assertTrue(all(r.is_cancelled == 0 for r in rows))

    def test_reverse_entries_on_cancel(self):
        je = make_journal_entry().insert()
        je.submit()
        je.cancel()

        rows = gl_rows("Journal Entry", je.name)
        self.assertEqual(len(rows), 4)
        self.assertTrue(all(r.is_cancelled == 1 for r in rows))
        self.assertEqual(
            sum(r.debit_amount for r in rows), sum(r.credit_amount for r in rows)
        )
        cash_net = sum(r.debit_amount - r.credit_amount for r in rows if r.account == CASH)
        self.assertEqual(cash_net, 0)

    def test_unbalanced_journal_entry_rejected(self):
        je = make_journal_entry(debit=1000, credit=900)
        self.assertRaises(frappe.ValidationError, je.insert)

    def test_payment_entry_wrong_party_type_rejected(self):
        party_name = "Test Supplier For Payment"
        if not frappe.db.exists("Party", party_name):
            frappe.get_doc(
                {"doctype": "Party", "party_name": party_name, "party_type": "Supplier"}
            ).insert()

        pe = frappe.get_doc(
            {
                "doctype": "Payment Entry",
                "posting_date": "2026-11-18",
                "payment_type": "Receive",
                "party_type": "Customer",
                "party": party_name,
                "account_paid_from": SALES,
                "account_paid_to": CASH,
                "amount": 500,
            }
        )
        self.assertRaises(frappe.ValidationError, pe.insert)