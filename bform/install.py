import click

from bform.setup import after_install as setup


def after_install():
	try:
		click.secho("Setting up bform", fg="blue")
		setup()
	except Exception as e:
		click.secho(f"Error setting up bform: {e}", fg="red")
		click.secho("Rolling back...", fg="red")
		click.secho("bform setup failed, please reinstall or create a bug report", fg="red")
		raise e
