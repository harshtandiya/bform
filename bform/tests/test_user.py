import frappe
import frappe.permissions
from faker import Faker
from frappe.tests import IntegrationTestCase

from .utils import create_test_user


class TestUser(IntegrationTestCase):
	def setUp(self):
		self.user = create_test_user()

	def tearDown(self):
		frappe.set_user("Administrator")
		self.user.delete(force=True)

	def test_set_role(self):
		# Given that `set_roles_at_sign_up` is enabled in Bform Settings
		frappe.db.set_single_value(
			"Bform Settings",
			"set_roles_at_sign_up",
			1,
		)
		self.assertTrue(
			frappe.db.get_single_value(
				"Bform Settings",
				"set_roles_at_sign_up",
			)
		)
		# When a new user is created
		new_user = create_test_user()

		# Then that user should have the "BForm User" Role
		roles = frappe.get_roles(new_user.name)
		self.assertTrue("BForm User" in roles)

	def test_team_creation(self):
		# Given when a user is created: self.user
		# Then a team with the user as it's member should be created.
		self.assertTrue(frappe.db.exists("Bform Team Member", {"user": self.user.name}))

	def test_on_trash(self):
		# Given a user
		user = create_test_user()
		user_team = frappe.get_doc(
			"Bform Team", frappe.db.get_value("Bform Team Member", {"user": user.name}, "parent")
		)
		self.assertTrue(user_team)
		user.delete()
		self.assertEqual(frappe.db.count("Bform Team Member", {"user": user.name}), 0)
