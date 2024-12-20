import click

from bform.setup import after_uninstall as uninstall


def after_uninstall():
	try:
		click.secho("Uninstalling bform", fg="blue")
		uninstall()
	except Exception as e:
		click.secho(f"Error uninstalling bform: {e}", fg="red")
		click.secho("Rolling back...", fg="red")
		click.secho("bform uninstall failed, please reinstall or create a bug report", fg="red")
		raise e
