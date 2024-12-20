import click
import frappe


def after_install():
	setup_roles()


def after_uninstall():
	delete_roles()


def get_custom_roles():
	roles = [
		{"role": "BForm User", "desk_access": 0},
	]
	return roles


def setup_roles():
	roles = get_custom_roles()
	click.secho("Creating roles for bform...", fg="blue")

	for role in roles:
		click.secho(f"Creating role: {role.get('role')}...")
		if not frappe.db.exists("Role", role.get("role")):
			frappe.get_doc(
				{"doctype": "Role", "role_name": role.get("role"), "desk_access": role.get("desk_access")}
			).insert(ignore_permissions=True)


def delete_roles():
	roles = get_custom_roles()
	click.secho("Deleting roles for bform...", fg="blue")

	for role in roles:
		click.secho(f"Deleting role: {role.get('role')}...")
		if frappe.db.exists("Role", role.get("role")):
			frappe.delete_doc("Role", role.get("role"), force=True)
