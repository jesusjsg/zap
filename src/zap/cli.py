import click
import os
from pathlib import Path


@click.group()
def cli():
    """Zap is a tool to say goodbye to your files"""
    pass


@click.group()
def files():
    """Files commands"""
    pass


@cli.command()
def version():
    """Version of zap"""
    click.echo("zap version 0.0.1")


if __name__ == "__main__":
    cli()
