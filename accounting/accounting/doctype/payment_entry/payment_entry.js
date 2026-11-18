frappe.ui.form.on("Payment Entry", {
	setup(frm) {
		frm.set_query("party", () => {
			return { filters: { party_type: frm.doc.party_type } };
		});
		frm.set_query("account_paid_from", () => {
			return { filters: { is_group: 0, account_type: ["in", ["Asset", "Liability"]] } };
		});
		frm.set_query("account_paid_to", () => {
			return { filters: { is_group: 0, account_type: ["in", ["Asset", "Liability"]] } };
		});
	},

	payment_type(frm) {
		let type = frm.doc.payment_type === "Receive" ? "Customer" : "Supplier";
		frm.set_value("party_type", type);
	},

	party_type(frm) {
		frm.set_value("party", "");
	},
});
