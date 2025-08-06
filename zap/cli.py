import click
from pathlib import Path

from zap.core import clean_and_move_files, delete_files, list_files
from .utils import print_output, validate_path


@click.group()
def cli():
    """Zap is a tool to say goodbye to your files"""
    pass


@cli.command()
@click.option(
    "--ext", "-e", type=click.STRING, help="Listing files with extension"
)
@click.option("--long", "-l", is_flag=True, help="Long listing")
@click.argument(
    "path", type=click.Path(exists=True, path_type=Path), default="."
)
def zl(path: Path, ext: str | None, long: bool) -> None:
    """List current directory files"""
    validate_path(path)
    for name, color in list_files(path, ext, long, print_output):
        click.secho(f"{name}", fg=color)


@cli.command()
@click.option(
    "--ext",
    "-e",
    type=click.STRING,
    help="File extension to zap the files (e.g .py)",
)
@click.argument("path", type=click.Path(exists=True, path_type=Path))
def zd(path: Path, ext: str | None) -> None:
    """Zap current directory files"""
    validate_path(path)
    result = delete_files(path, ext)
    click.secho(result, fg="green")


@cli.command()
@click.option("--ext", "-e", type=click.STRING, help="File type to order")
@click.argument(
    "path",
    type=click.Path(exists=True, path_type=Path),
    default=Path.home().joinpath("Downloads"),
)
def zc(path: Path, ext: str | None) -> None:
    """Clean your downloads directory"""
    validate_path(path)
    results = clean_and_move_files(path, ext)
    for m in results:
        fg = "green" if m.startswith("Moved") else "yellow"
        click.secho(m, fg=fg)


@cli.command()
def version():
    """Version of zap"""
    click.secho("zap version 0.0.1", fg="green")
