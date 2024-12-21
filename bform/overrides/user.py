import frappe


def after_insert(doc, method=None):
	set_roles(doc, method)
	create_user_team(doc)


def on_trash(doc, method):
	delink_users_from_team(doc)


def set_roles(doc, method):
	set_roles_at_sign_up = frappe.db.get_single_value("BForm Settings", "set_roles_at_sign_up")

	if not set_roles_at_sign_up:
		return
	user = frappe.get_doc("User", doc.name)
	user.flags.ignore_permissions = True
	user.add_roles("BForm User")


def create_user_team(doc):
	team = frappe.get_doc(
		{
			"doctype": "Bform Team",
			"team_name": f"{doc.email}",
			"members": [{"user": doc.name}],
		}
	)

	team.insert(ignore_permissions=True)


def delink_users_from_team(doc):
	member_doctypes = frappe.get_all("Bform Team Member", {"user": doc.name}, pluck="name")
	for member in member_doctypes:
		frappe.delete_doc("Bform Team Member", member, force=True)
