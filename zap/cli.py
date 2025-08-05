import click
from pathlib import Path
from .utils import validate_extension, print_output, validate_path


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

    for file in sorted(path.iterdir()):
        if file.is_dir() and ext:
            continue
        if file.is_file() and not validate_extension(file, ext):
            continue
        name, color = print_output(file, long)
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
@click.option("--ext", "-e", type=click.STRING, help="File type to order")
@click.argument(
    "path",
    type=click.Path(exists=True, path_type=Path),
    default=Path.home().joinpath("Downloads"),
)
def zc(path: Path, ext: str | None) -> None:
    """Clean your current directory"""
    validate_path(path)
    home_path = path.home()

    for file in path.iterdir():
        if file.is_file() and validate_extension(file, ext):
            extension = file.suffix.lower().lstrip(".")
            destination_path = home_path.joinpath("Documents", extension)
            destination_path.mkdir(parents=True, exist_ok=True)
            output = destination_path.joinpath(file.name)
            file.rename(output)


@cli.command()
def version():
    """Version of zap"""
    click.secho("zap version 0.0.1", fg="green")
