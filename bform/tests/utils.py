import frappe
from faker import Faker

fake = Faker()


def create_test_user(**kwargs):
	user = frappe.get_doc(
		{
			"doctype": "User",
			"email": kwargs.get("email", fake.email()),
			"first_name": kwargs.get("first_name", fake.name()),
		}
	)
	user.insert(ignore_permissions=True)
	user.reload()
	return user
