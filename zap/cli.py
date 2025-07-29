import click
from pathlib import Path
from .utils import validate_extension, get_file_info, validate_path


def _print_output(file: Path, long: bool = False) -> None:
    if long:
        size, user, group, date, name = get_file_info(file)
        click.secho(f"{size}\t {user} \t {group} \t {date}\t", nl=False)
    name = f"{file.name}" if file.is_dir() else file.name
    color = "blue" if file.is_dir() else "green"
    click.secho(name, fg=color)


@click.group()
def cli():
    """Zap is a tool to say goodbye to your files"""
    pass


@cli.command()
@click.option(
    "-e", "--ext", type=click.STRING, help="Listing files with extension"
)
@click.option("-l", "--long", is_flag=True, help="Long listing")
@click.argument(
    "path", type=click.Path(exists=True, path_type=Path), default="."
)
def zl(path: Path, ext: str | None, long: bool) -> None:
    """List current directory files"""
    validate_path(path)

    for file in path.iterdir():
        if file.is_dir() and ext:
            continue
        if file.is_file() and not validate_extension(file, ext):
            continue
        _print_output(file, long)


@cli.command()
@click.option(
    "-e",
    "--ext",
    type=click.STRING,
    help="File extension to zap the files (e.g .py)",
)
@click.argument("path", type=click.Path(exists=True, path_type=Path))
def zd(path: Path, ext: str | None) -> None:
    """Zap current directory files"""
    validate_path(path)

    if ext:
        for file in path.iterdir():
            if file.is_file() and not validate_extension(file, ext):
                continue
            if file.is_dir():
                continue
            file.unlink()
        click.secho(f"Zapped files with extension {ext}")
    else:
        for file in path.iterdir():
            if file.is_file():
                file.unlink()
        path.rmdir()
        click.secho(f"Zapped dir {path.name}")


@cli.command()
@click.option("-e", "--ext")
def version():
    """Version of zap"""
    click.secho("zap version 0.0.1", fg="green")
