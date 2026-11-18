frappe.ui.form.on("Sales Invoice", {
	setup(frm) {
		frm.set_query("customer", () => {
			return { filters: { party_type: "Customer" } };
		});
		frm.set_query("debit_to", () => {
			return { filters: { account_type: "Asset", is_group: 0 } };
		});
		frm.set_query("income_account", () => {
			return { filters: { account_type: "Income", is_group: 0 } };
		});
	},
});

frappe.ui.form.on("Sales Invoice Item", {
	item(frm, cdt, cdn) {
		let row = locals[cdt][cdn];
		if (!row.item) return;
		frappe.db.get_value("Item", row.item, "standard_selling_rate").then((r) => {
			frappe.model.set_value(cdt, cdn, "rate", r.message.standard_selling_rate || 0);
		});
	},
	qty(frm, cdt, cdn) {
		update_row(frm, cdt, cdn);
	},
	rate(frm, cdt, cdn) {
		update_row(frm, cdt, cdn);
	},
});

function update_row(frm, cdt, cdn) {
	let row = locals[cdt][cdn];
	frappe.model.set_value(cdt, cdn, "amount", (row.qty || 0) * (row.rate || 0));
}
