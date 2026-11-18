frappe.ui.form.on("Journal Entry", {
	setup(frm) {
		frm.set_query("account", "accounts", () => {
			return { filters: { is_group: 0 } };
		});
	},
});

frappe.ui.form.on("Journal Entry Account", {
	debit(frm) {
		update_totals(frm);
	},
	credit(frm) {
		update_totals(frm);
	},
	accounts_remove(frm) {
		update_totals(frm);
	},
});

function update_totals(frm) {
	let total_debit = 0;
	let total_credit = 0;
	(frm.doc.accounts || []).forEach((row) => {
		total_debit += flt(row.debit);
		total_credit += flt(row.credit);
	});
	frm.set_value("total_debit", total_debit);
	frm.set_value("total_credit", total_credit);
	frm.set_value("difference", total_debit - total_credit);
}
